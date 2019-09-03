from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from blog.models import Post, Category, Tag
from comment.forms import CommentForm
from comment.models import Comment
from config.models import SideBar


# def test_get_post_log_entry(request, post_pk):
#     post = Post.objects.get(id=post_pk)
#     log_entries = LogEntry.objects.filter(content_type_id=get_content_type_for_model(post).pk, object_id=post.pk)
#     return HttpResponse(log_entries)


# def post_list(request, category_id=None, tag_id=None):
#     category = None
#     tag = None
#
#     if category_id:
#         post_list, category = Post.get_by_category(category_id)
#     elif tag_id:
#         post_list, tag = Post.get_by_tag(tag_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category': category,
#         'tag': tag,
#         'post_list': post_list,
#         'sidebars': SideBar.get_all(),
#     }
#
#     context.update(Category.get_navs())
#     return render(request, 'blog/list.html', context=context)


# def post_detail(request, post_id):
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         post = None
#
#     context = {
#         'post': post,
#         'sidebars': SideBar.get_all(),
#     }
#
#     context.update(Category.get_navs())
#     return render(request, 'blog/detail.html', context=context)


class CommonViewMixin:
    """导入侧边栏和分类导航context"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    """主页文章类视图"""

    queryset = Post.latest_posts()
    context_object_name = 'post_list'
    template_name = 'blog/list.html'
    paginate_by = 5


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path),
        })
        return context


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)
