from asyncio.windows_events import NULL
from django.shortcuts import render,redirect,get_object_or_404,reverse
from user.forms import LoginForm,RegisterForm,ChangePasswordForm,UpdateUserInfoForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None) # Bu kısım sayesinde GET veya POST request alıp almadığımızı kontrol etmiş oluyoru
    if form.is_valid(): #yazdığımız clean metodu sadece burada çağırılır
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
            
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        login(request,newUser) #Django'nun kendi login fonksiyonu
        messages.success(request,"Başarıyla Kayıt Oldunuz...")
        return redirect("index")
    else:
        context = {
                "form":form
            }
    return render(request,"register.html",context)
        
        
def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(username = username,password = password)#Django'nun kendi authenticate(doğrulama) fonksiyonu
        if user is None: #Böyle bir user'ımız yoksa.
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)
        else:
            messages.success(request,"Başarıyla Giriş Yaptınız...")
            login(request,user)
            return redirect("index")
    #Herhangi bir GET request olmama durumunda
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız...")
    return redirect("index")

def changePassword(request):
    form = ChangePasswordForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = get_object_or_404(User,username=username)
        #user = User.objects.get(username=username)
          
        if username == user.username: #Obje tip str olmadığı için direkt eşitlik kontrolü yapamıyoruz. str'ye çevirdik
            user.set_password(password)
            user.save()
            messages.success(request,"Şifre Başarıyla Güncellendi!")
            return redirect("user:login")
        else:
            messages.info(request,"Bu nickname'e sahip bir kullanıcı bulunamadı...")
            return render(request,"changepassword.html",{"form":form})
        
    return render(request,"changepassword.html",{"form":form})

def profile(request,id): #Sadece Kullanıcı Bilgilerini Alacaktır
    userinfos = User.objects.get(id=id) #Bu sayede bütün article'ları almış olacağız.
    print(userinfos.username)
    print(userinfos.email)
    return render(request,"profile.html",{"userinfos":userinfos})

def updateUserInfo(request,id):
    user = get_object_or_404(User,id=id)
    form = UpdateUserInfoForm(request.POST or None)
    form.username = user.username
    form.password = user.password
    print(form.username)
    print(form.password)
    #form.email = user.email
    if form.is_valid():
        newusername = form.cleaned_data.get('username')
        newpassword = form.cleaned_data.get('password')
        newemail = form.cleaned_data.get('email')
        user.username = newusername
        user.set_password(newpassword) 
        user.email = newemail  
        user.save()
        login(request,user)
        messages.success(request,"Kullanıcı Bilgileri Başarıyla Güncellendi!")
        return redirect("index")

    return render(request,"updateuserinfo.html",{"form":form})
        
    