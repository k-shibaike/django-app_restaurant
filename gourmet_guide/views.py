from django.urls import reverse_lazy
from django.views import generic
from .models import Category, Shop
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import ShopCreateForm

import requests
import urllib

class IndexView(generic.ListView):
    model = Shop

class DetailView(generic.DetailView):
    # ↓ 使用するテンプレートファイルを指定
    template_name = 'gourmet_guide/wonderful_shop_detail.html'
    model = Shop

    # テンプレートにデータを渡すため
    def get_context_data(self, **kwargs):
        # 親クラスのメソッドを呼び出し
        context = super().get_context_data(**kwargs)
        
        # Shopモデルのインスタンスから住所フィールドを取得
        shop_instance = self.get_object()
        address = shop_instance.address

        # (国土地理院のAPI)
        ## エンドポイント
        makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
        # エンコード(https://tech-unlimited.com/urlencode.html)
        s_quote = urllib.parse.quote(address)
        # print("S_quote", s_quote)

        response = requests.get(makeUrl + s_quote)
        print("response", response)

        coordinates = response.json()[0]["geometry"]["coordinates"]
        print("coordinates", coordinates)

        reversed_coordinates = reversed(coordinates)

        context['coordinates'] = ",".join(map(str, reversed_coordinates))
        print("context['coordinates']", context['coordinates'])

        return context

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Shop
    form_class = ShopCreateForm

    # フォームデータを取得し、データベースに保存するなどの操作を行う
    def form_valid(self, form):
        # authorにログインしているユーザー名を代入
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Shop
    fields = ['name', 'address', 'category', 'image'] 

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Shop
    success_url = reverse_lazy('gourmet_guide:index')