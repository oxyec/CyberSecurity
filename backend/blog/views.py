from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
import bleach

ALLOWED_TAGS = [
    'p', 'b', 'i', 'u', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'br', 'span', 'blockquote', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
]
ALLOWED_ATTRIBUTES = {
    '*': ['style'],
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
    'span': ['style'],
}

def blog_list(request):
    # Optimize: Fetch authors with posts to avoid N+1 query problem
    posts = Post.objects.select_related('author').all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def post_detail(request, pk):
    # Optimize: Fetch author with post
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
    comments = post.comments.filter(parent__isnull=True)
    comment_form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.content = bleach.clean(
                comment.content,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                strip=True
            )
            comment.save()
            return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  
            post.content = bleach.clean(
                post.content,
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                strip=True
            )
            post.save()
            return redirect('blog_list')
    else:
        form = PostForm()
    return render(request, 'blog/blog_create.html', {'form': form})
