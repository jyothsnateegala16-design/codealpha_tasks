from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('create/', views.create_post, name='create_post'),
    path('profile/', views.profile, name='profile'),


    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/edit/<int:id>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:id>/', views.delete_post, name='delete_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),

    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    
    path('upload-image/', views.upload_profile_image, name='upload_image'),
    
]


