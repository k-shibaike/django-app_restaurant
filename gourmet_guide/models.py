from django.db import models
from django.urls import reverse


# カテゴリモデル: 飲食店のカテゴリ（例: フレンチ、イタリアン、寿司など）を表現
class Category(models.Model):
    # カテゴリの名前を格納する文字列フィールド
    name = models.CharField(max_length=255)
    
    # カテゴリを作成したユーザーとのリレーションシップを表現
    author = models.ForeignKey(
        'auth.User',  # Djangoのデフォルトのユーザーモデルを指定
        on_delete=models.CASCADE,  # ユーザーが削除された場合、関連するカテゴリも削除
    )
    
    # カテゴリの作成日時を格納する日時フィールド（自動的に追加される）
    created_at = models.DateTimeField(auto_now_add=True)
    
    # カテゴリの更新日時を格納する日時フィールド（自動的に更新される）
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # カテゴリの名前を文字列として返す（管理画面などで表示される）
        return self.name

# 店舗モデル: 飲食店の情報を表現
class Shop(models.Model):
    # 飲食店の名前を格納する文字列フィールド
    name = models.CharField(max_length=255)
    
    # 飲食店の住所を格納する文字列フィールド
    address = models.CharField(max_length=255)

    # 画像pathを保存するためのフィールド
    image = models.ImageField(upload_to='images', null=True)
    
    # 飲食店を作成したユーザーとのリレーションシップを表現
    author = models.ForeignKey(
        'auth.User',  # Djangoのデフォルトのユーザーモデルを指定
        on_delete=models.CASCADE,  # ユーザーが削除された場合、関連する店舗も削除
    )
    
    # 飲食店のカテゴリとのリレーションシップを表現
    category = models.ForeignKey(
        Category,  # カテゴリモデルとのリレーションシップ
        on_delete=models.PROTECT,  # 関連するカテゴリが削除ても削除されない
    )
    
    # 飲食店の作成日時を格納する日時フィールド（自動的に追加される）
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 飲食店の更新日時を格納する日時フィールド（自動的に更新される）
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # 飲食店の名前を文字列として返す（管理画面などで表示される）
        return self.name
    
    def get_absolute_url(self):
        return reverse('gourmet_guide:detail', kwargs={'pk': self.pk})
