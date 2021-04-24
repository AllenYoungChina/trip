from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileEditForm
from .models import User, Profile


@admin.register(User)
class MyUserAdmin(UserAdmin):
    """ 用户基础信息 """
    list_display = ('username', 'nickname', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'nickname')
    # 新增用户时的表单字段
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nickname', )}),
    )
    # 修改用户时的表单字段
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nickname', 'avatar')}),
    )
    # 批量操作
    actions = ('disable_user', 'enable_user')

    def disable_user(self, request, queryset):
        """ 批量禁用用户 """
        queryset.update(is_active=False)

    def enable_user(self, request, queryset):
        """ 批量启用用户 """
        queryset.update(is_active=True)

    # 配置批量操作方法的中文名称
    disable_user.short_description = '批量禁用用户'
    enable_user.short_description = '批量启用用户'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ 用户详细信息 """
    list_display = ('format_username', 'sex', 'age', 'created_at')
    list_per_page = 10
    list_select_related = ('user', )
    list_filter = ('sex', )
    search_fields = ('username', 'user__nickname')
    fields = ('real_name', 'email', 'phone_no', 'sex', 'age')
    # 自定义表单验证
    form = ProfileEditForm

    def format_username(self, obj):
        return obj.username[:3] + '****' + obj.username[-4:]

    format_username.short_description = '用户名'
