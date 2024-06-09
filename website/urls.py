from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('', views.HomeView.as_view(), name='waste'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('all_posts', views.AllPostsView.as_view(), name='all_posts'),
    path('liked/<int:pk>/', views.likeView, name='post_like'),
    path('comment/<int:pk>/', views.commentView, name='post_comment', )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
