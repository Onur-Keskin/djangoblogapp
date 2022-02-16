from django import forms
from .models import Article
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article #elindeki modelle burdaki formu ilişkili hale getirmek için
        fields = ["title","content","article_image"]

    