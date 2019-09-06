from django.contrib import admin


class BaseOwnerAdmin:
    """
    1.后台表单保存时候，自动补全owner字段
    2.只显示当前用户内容
    """

    exclude = ('owner',)

    # Django admin写法

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
    #
    # def get_queryset(self, request):
    #     qs = super(BaseOwnerAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # xadmin写法
    def save_models(self):
        self.new_obj.owner = self.request.user
        super().save_models()

    def get_list_queryset(self):
        qs = super().get_list_queryset()
        return qs.filter(owner=self.request.user)
