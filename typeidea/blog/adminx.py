import xadmin
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html
from xadmin.filters import RelatedFieldListFilter, manager
from xadmin.layout import Fieldset, Row, Container

from blog.adminforms import PostAdminForm
from blog.models import Category, Tag, Post
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


# xadmin写法（演示用）
class PostInline:
    model = Post
    extra = 1  # 可以添加几篇文章
    form_layut = (
        Container(
            Row('title', 'desc'),
        )
    )


@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = (PostInline,)
    # list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count',)
    fields = ('name', 'status', 'is_nav',)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


# class CategoryOwnerFilter(SimpleListFilter):
#     """自定义过滤器 - 显示当前用户自己的分类"""
#
#     title = "分类过滤器"
#     parameter_name = 'owner_category'
#
#     def lookups(self, request, model_admin):
#         return Category.objects.filter(owner=request.user).values_list('id', 'name')
#
#     def queryset(self, request, queryset):
#         category_id = self.value()
#         if category_id:
#             return queryset.filter(category_id=category_id)
#         return queryset

class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
    # form = PostAdminForm

    list_display = (
        'title', 'category', 'status', 'created_time', 'operator',)
    list_display_links = ()

    list_filter = ('category',)
    search_fields = ('title', 'category__name')

    # 顶部、底部显示操作动作栏（删除等）
    actions_on_top = True
    actions_on_bottom = True

    # 顶部也显示保存按钮
    save_on_top = True

    # exclude = ('owner',)

    # 包裹在元组内的字段，显示在同一行
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # fieldsets = (
    #     ('基础配置', {
    #         'description': '基础配置描述',
    #         'fields': (
    #             ("title", "category"),
    #             'status',
    #         )
    #     }),
    #     ('内容', {
    #         'fields': (
    #             'desc',
    #             'content',
    #         )
    #     }),
    #     ('额外信息', {
    #         'classes': ('wide',),
    #         'fields': ('tag',)
    #     }),
    # )

    form_layout = (
        Fieldset(
            '基础信息',
            Row('title', 'category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
        ),
    )

    # filter_horizontal = ('tag',)

    # filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

# @xadmin.sites.register(LogEntry)
# class LogEntryAdmin:
#     list_display = ('object_repr', 'user', 'object_id', 'action_flag', 'change_message')
