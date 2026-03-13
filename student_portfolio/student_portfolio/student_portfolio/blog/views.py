from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
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
@login_required
def like_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'count': post.likes.count()})


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated!')
            return redirect('blog_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_slug = comment.post.slug
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted.')
        return redirect('blog_detail', slug=post_slug)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})
