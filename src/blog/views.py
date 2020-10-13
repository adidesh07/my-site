from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlogPostForm, UpdateBlogPostForm, BlogPostCommentForm
from account.models import Account
from django.db.models import Q
from django.http import HttpResponse
from .models import BlogPost
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
# Create your views here.


def create_blog_view(request):
    context = {}
    
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')  

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(username=user.username).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
        return redirect('home')

    context['form'] = form

    return render(request, 'blog/create_blog.html', {})


def detail_blog_view(request, slug):
    context = {}
    user = request.user

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    if request.POST and user.is_authenticated:
        form = BlogPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = blog_post
            comment.author = user.username
            comment.save()
            form = BlogPostCommentForm()
            return redirect('home')
    else:
        form = BlogPostCommentForm()
    context['form'] = form

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse('Oops! You are not the author of this post and hence, cannot edit it.')

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = 'Updated Successfully!'
            blog_post = obj

    form = UpdateBlogPostForm(
        initial={
            'title': blog_post.title,
            'body': blog_post.body,
            'image': blog_post.image
        }
    )
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)


def delete_post_view(request, slug):
    user = request.user
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse('Oops! You are not the author of this post and hence, cannot edit it.')

    if user.is_authenticated and request.POST:
        blog_post.delete()
        context['success_message'] = 'Post deleted successfully!'
    return render(request, 'blog/confirm_delete.html', context)


def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(' ')
    for q in queries:
        posts = BlogPost.objects.filter(
                Q(title__icontains=q) |
                Q(body__icontains=q)
            ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))








