from django.contrib import admin


class BaseOwnerAdmin:
    """
    1.后台表单保存时候，自动补全owner字段
    2.只显示当前用户内容
    """

    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
