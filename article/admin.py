from django.contrib import admin

from .models import Article,Comment
# Register your models here.

admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","author","created_date"] #Attributeleri dışarda gösterir.
    list_display_links = ["title","created_date"] #Belirtilen içerikleri linkler.
    
    search_fields = ["title"] #Arama Çubuğu ekler
    
    list_filter = ["created_date"] #İçeri girilen değere göre filtreleme işlemi yapar.
    
    class Meta:
        model = Article #Article ile ArticleAdmin'i bağlamak için bu işlemi yaptık.Django dokümanı böyle belirtti
        