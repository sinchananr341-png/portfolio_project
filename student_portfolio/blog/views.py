from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm


def blog_list(request):
    posts = BlogPost.objects.filter(status='published')
    return render(request, 'blog/blog_list.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if post.status == 'draft' and (not request.user.is_authenticated or request.user != post.author):
        from django.http import Http404
        raise Http404
    
    comments = post.comments.filter(parent__isnull=True)
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('blog_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/blog_detail.html', {
        'post': post, 
        'comments': comments,
        'comment_form': comment_form
    })


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created!')
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'New Blog Post'})


@login_required
def blog_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated!')
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/blog_form.html', {'form': form, 'title': 'Edit Blog Post'})


@login_required
def blog_delete(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted.')
        return redirect('dashboard')
    return render(request, 'blog/blog_confirm_delete.html', {'post': post})
