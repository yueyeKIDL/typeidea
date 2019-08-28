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
    category = None
    tag = None

    if category_id:
        post_list, category = Post.get_by_category(category_id)
    elif tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    }
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})
