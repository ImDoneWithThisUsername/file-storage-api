from django.urls import path
from .views import *
urlpatterns = [
    path('user/images', UserImagesView.as_view()),
    path('user', UserInfoView.as_view()),
    path('user/register', UserRegisterView.as_view()),
    path('user/images/<int:pk>', DownloadImageView.as_view()),
    path('user/images/share', ShareImageView.as_view()),
]
