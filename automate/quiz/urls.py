from django.conf.urls import url
from django.contrib.auth.views import login, logout, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

app_name = 'quiz'
urlpatterns = [
    url(r'^prev/', views.preverify, name='prev'),
    url(r'^v/', views.verify, name='verify'),

]
