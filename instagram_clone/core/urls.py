from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('chat/<str:username>/', views.chat, name='chat'),
]
    