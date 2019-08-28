from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Post, Category, Tag


def test_get_post_log_entry(request, post_pk):
    post = Post.objects.get(id=post_pk)
    log_entries = LogEntry.objects.filter(content_type_id=get_content_type_for_model(post).pk, object_id=post.pk)
    return HttpResponse(log_entries)


def post_list(request, category_id=None, tag_id=None):
    if category_id:
        post_list = Post.objects.filter(category_id=category_id, status=Post.STATUS_NORMAL)
    elif tag_id:
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)

    return render(request, 'blog/list.html', context={'post_list': post_list})


def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})
