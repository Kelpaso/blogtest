from django.urls import path
from django.contrib.auth import views as viewsGlobal
from . import views as viewsLocal

urlpatterns = [
    path('', viewsLocal.post_list, name='post_list'),
    path('accounts/login/', viewsLocal.sing_in, name='login'),
    path('accounts/logout/', viewsLocal.logout_user, name='logout'),
    path('post/<int:pk>/', viewsLocal.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', viewsLocal.post_edit, name='post_edit'),
    path('post/new/', viewsLocal.post_new, name='post_new'),
    path('drafts/', viewsLocal.post_draft_list, name='post_draft_list'),
    path('post/<pk>/publish/', viewsLocal.post_publish, name='post_publish'),
    path('post/<pk>/remove/', viewsLocal.post_remove, name='post_remove'),
]
