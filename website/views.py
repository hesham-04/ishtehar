from django.views.generic import ListView, DetailView, CreateView
from accounts.models import Post, User, Like
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Create your views here.


def likeView(request, pk):
    post = get_object_or_404(Post, id=pk)
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()

    return redirect('post_detail', pk=post.id)







class HomeView(ListView):
    model = Post
    template_name = 'website/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Most liked post
        context['most_liked_post'] = Post.objects.annotate(like_count=Count('like')).filter(like_count__gt=0).order_by('-like_count').first()
        # Trending post (assuming you have a way to determine popularity, e.g., by number of likes and comments combined)
        context['trending_post'] = Post.objects.annotate(like_count=Count('like'), comment_count=Count('comment')).order_by('-like_count', '-comment_count').first()
        # Most popular posts (assuming you have a way to determine popularity, e.g., by number of likes)
        context['most_popular_posts'] = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')[:3]
        # Recent posts
        context['recent_posts'] = Post.objects.order_by('-created_at')[:5]
        # List of authors
        context['authors'] = User.objects.annotate(post_count=Count('post')).order_by('-post_count')[:5]
        
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'website/create_post.html'
    fields = ['title', 'content', 'image', 'tags']
    login_url = 'accounts:login'
    success_url = reverse_lazy('waste')  # Change to your desired success URL

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'website/post_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        is_liked = False
        if self.request.user.is_authenticated and Like.objects.filter(user=self.request.user, post=post).exists():
            is_liked = True

        context['post'] = post
        context['is_liked'] = is_liked
        context['total_likes'] = Like.objects.filter(post=post).count()
        return context

class DashboardView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'website/user_details.html'
    context_object_name = 'user_details'

    def get_object(self, queryset=None):
        # Return the current authenticated user as the object for detail view
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = self.get_object().post_set.count()
        context['posts'] = self.get_object().post_set.all()
        return context




class UserProfileView(DetailView):
    model = User
    template_name = 'website/user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object  # This is already available from DetailView

        context['post_count'] = user.post_set.count()
        context['posts'] = user.post_set.all()
        return context



class AllPostsView(ListView):
    model = Post
    template_name = 'website/all_posts.html'
    context_object_name = 'all_posts'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')
