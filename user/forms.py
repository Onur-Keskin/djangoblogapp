import email
from django import forms
from  django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola",widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label="Kullanıcı Adı",min_length=2)
    password = forms.CharField(max_length=20,label="Parola",min_length=3,widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parolayı Doğrula",widget=forms.PasswordInput)
    
    def clean(self): #Parolayı doğruluğunu kontrol edebilmek için django tarafından önerilen fonksiyon
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı kullanılıyor...')
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor") # Hata fırlatma
        
        #Bir sonraki sayfaya mutlaka sözlük yapısıyla dönmek gerekiyor
        values = {
            "username":username,
            "password":password,
        }
        return values
"""
class ChangePasswordForm1(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
"""
class ChangePasswordForm(forms.Form):
    username = forms.CharField(max_length=50,label="Kullanıcı Adı",min_length=2)
    password = forms.CharField(max_length=20,label="Parola",min_length=3,widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parolayı Doğrula",widget=forms.PasswordInput)
    
    def clean(self): #Parolayı doğruluğunu kontrol edebilmek için django tarafından önerilen fonksiyon
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor") # Hata fırlatma
        
        #Bir sonraki sayfaya mutlaka sözlük yapısıyla dönmek gerekiyor
        values = {
            "username":username,
            "password":password,
        }
        return values

class UpdateUserInfoForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Parola",widget=forms.PasswordInput)
    
    
    confirm = forms.CharField(max_length=20,label="Parolayı Doğrula",widget=forms.PasswordInput)
    
    def clean(self): #Parolayı doğruluğunu kontrol edebilmek için django tarafından önerilen fonksiyon
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        
        
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Bu kullanıcı adı kullanılıyor...')
               
        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor") # Hata fırlatma
        
        #Bir sonraki sayfaya mutlaka sözlük yapısıyla dönmek gerekiyor
        values = {
            "username":username,
            "password":password,
            "email":email,
        }
        return values