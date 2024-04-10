from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.user_register, name='user_register'),
    path('accounts/login/', views.sing_in, name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/posts/', views.profile_posts, name='profile_posts'),
    path('profile/comments/', views.profile_comments, name='profile_comments'),
    path('profile/delete/', views.profile_delete, name='profile_delete'),
    path('profile/email/confirm/', views.email_confirm, name='email_confirm'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]
