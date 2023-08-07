from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from blog.forms import PostCreationForm
from blog.models import Category, Post


class IndexView(View):
    def get(self, request):
        featured_post = Post.objects.order_by('-views').first()
        trending_posts = Post.objects.all().exclude(id=featured_post.id)[:5]
        random_posts = Post.objects.order_by(
            '?').exclude(id=featured_post.id)[:9]
        categories = Category.objects.order_by('name')

        ctx = {
            'featured_post': featured_post,
            'trending_posts': trending_posts,
            'random_posts': random_posts,
            'categories': categories
        }
        return render(request, 'blog/index.html', ctx)


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostCreationForm()
        return render(request, 'blog/form.html', {'form': form})

    def post(slef, request):
        form = PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = post.title
            messages.success(request, 'Blog post created successfully')
            return redirect('index')
        print(request.POST)
        print('\n\n\n\n ######################')
        print(form.errors.as_data())
        return render(request, 'blog/form.html', {'form': form})


class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'blog/detail.html', {'post': post})
