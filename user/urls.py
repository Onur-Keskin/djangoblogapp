from django.contrib import admin
from django.urls import path
from . import views 

app_name = "user"

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('logout/',views.logoutUser,name="logout"),
    path('changepassword/',views.changePassword,name="changepassword"),
    path('profile/<int:id>',views.profile,name="profile"),
    path('updateuserinfo/<int:id>',views.updateUserInfo,name="updateuserinfo"),
    
]