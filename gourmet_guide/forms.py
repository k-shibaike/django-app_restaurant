from django import forms
from django.core.exceptions import ValidationError
from hashlib import sha256
from .models import Shop

import time

class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ["name", "address", "category", "image"]

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # 1. 画像ファイルの拡張子を確認
            allowed_extensions = ['jpg','jpeg','png']
            file_extension = image.name.lower().split('.')[-1]
            print("file_extension",file_extension)
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise ValidationError("JPEGまたはPNGフォーマットの画像ファイルをアップロードしてください。")

            # 2. ファイル名をハッシュ化
            time_int = int(time.time())
            hashed_filename = sha256(image.name.encode()).hexdigest()[:10] # ファイル名をハッシュ化して10文字までにする
            image.name = f"{hashed_filename}{str(time_int)}.{file_extension}"

        return image




