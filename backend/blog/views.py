from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm  # ← BU SATIR EKSİKTİ

def blog_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.save()
            posts = Post.objects.all().order_by('-created_at')
            return redirect('blog_list')

    else:
        form = PostForm()
    return render(request, 'blog/blog_create.html', {'form': form})
