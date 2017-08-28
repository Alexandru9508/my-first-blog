from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        '-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # messages.success(request, 'Form   successful')
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request, pk=None):
    instance = None
    if pk is not None:
        instance = get_object_or_404(Post, pk=pk)
        if instance.author != request.user:
            messages.error(request, ' Acces denied!')
            return redirect('post_list')
    if request.method == "POST":
        form = PostForm(request.POST, instance=instance)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Success!')
            return redirect('post_detail', pk=post.pk)
    form = PostForm(instance=instance)
    return render(request, 'blog/post_edit.html', {'form': form})


# def post_edit(request, pk=None):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})
