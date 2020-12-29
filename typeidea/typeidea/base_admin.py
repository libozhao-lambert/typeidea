from django.contrib import admin


# 共同类
class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章、分类、标签、侧边栏、友链这些Model的Owner字段
    2. 用来针对queryset过滤当前用户的数据（只显示该用户创建的内容）
    """

    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)