from turtle import title
from django.shortcuts import render,HttpResponse,render,redirect,get_object_or_404,reverse
from article.models import Article,Comment
from .forms import ArticleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
#Url geldiği zaman çalıştırılacak fonksiyonlar buraya yazılır.

def articles(request):
    keyword = request.GET.get("keyword")
    """
    Eğer bir arama işlemi olmayacaksa bütün makaleler sayfada gösterilecek fakat arama işlemi olursa sadece aranan makale gösterilecek.
    """
    if keyword: #Eğer articles sayfasında bir arama işlemi yapıldıysa.
        articles = Article.objects.filter(title__contains=keyword)
        return render(request,"articles.html",{"articles":articles})
    
    articles = Article.objects.all() #Bu sayede bütün article'ları almış olacağız.
    return render(request,"articles.html",{"articles":articles})


def index(request): #request parametresi her view fonksiyonunda ilk parametre olarak bulunması gerekir.
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

@login_required(login_url="user:login")#Eğer giriş yapmadan bu fonksiyona erişmek istersek bizi user uygulamasının altındaki login'e yönlendirecek
def dashboard(request):
    articles = Article.objects.filter(author=request.user)#Sisteme kim giriş yaptıysa onun article'leri alınacak
    context={
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    
    if form.is_valid():
        article=form.save(commit=False) #Formumuz model form'dan oluştuğu için sadece bu işlemi yapmak yetecektir. Fakat commit parametresiyle obje oluşturma işlemini kullanıcıya bırakır.
        article.author = request.user
        article.save() #Burayı tekrar neden yaptık ki?
        messages.success(request,"Makele Başarıyla Oluşturuldu")
        return redirect("article:dashboard")
    context = {
        "form":form
    }
    return render(request,"addarticle.html",context)

def detail(request,id):
    #article = Article.objects.filter(id=id).first() #Yakaladığı ilk bilgiyi alsın. Çünkü filter bize bir query list dönüyor
    article = get_object_or_404(Article,id=id)
    comments = article.comments.all()
    
    return render(request,"detail.html",{"article":article,"comments":comments})

@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id=id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance = article)#instance paremetresi ile article'ın içindeki bilgiler form'a yazılacaktır.
    
    if form.is_valid():
        article=form.save(commit=False) #Formumuz model form'dan oluştuğu için sadece bu işlemi yapmak yetecektir. Fakat commit parametresiyle obje oluşturma işlemini kullanıcıya bırakır.
        article.author = request.user
        article.save()
        messages.success(request,"Makele Başarıyla Güncellendi!")
        return redirect("article:dashboard")
    """    
    context = {
        "form":form
     }
    """
    return render(request,"update.html",{"form":form})

@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Makale Başarıyla Silindi.")
    
    return redirect("article:dashboard")#article uygulamasının altındaki dashboard'a git

def addComment(request,id):
    article = get_object_or_404(Article,id=id)
    
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        
        newComment = Comment(comment_author=comment_author, comment_content=comment_content)
        
        newComment.article = article
        
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id})) #/articles/detail/id(değişecek)