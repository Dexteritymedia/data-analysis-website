from django.urls import path, re_path, include
#from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('file-upload/', views.FileUpload.as_view(), name='file-upload'),
    path('upload-file/', views.file_form_upload, name='file-form-upload'),
    path('data-analysis/<file>/<slug>/', views.data_analysis, name='data-analysis'),
    path("sign-up/", views.RegisterView.as_view(), name='register'),
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_page, name="logout"),
]
