from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count',)
    fields = ('name', 'status', 'is_nav',)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(SimpleListFilter):
    """自定义过滤器 - 显示当前用户自己的分类"""

    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'status', 'created_time', 'operator',)
    list_display_links = ()

    list_filter = (CategoryOwnerFilter,)
    search_fields = ('title', 'category__name')

    # 顶部、底部显示操作动作栏（删除等）
    actions_on_top = True
    actions_on_bottom = True

    # 顶部也显示保存按钮
    save_on_top = True

    # 包裹在元组内的字段，显示在同一行
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
