from django.contrib import admin

# Register your models here.
from .models import Club

admin.site.register(Club)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Profile 모델을 UserAdmin에 인라인으로 추가
class ProfileInline(admin.StackedInline):  # 혹은 admin.TabularInline (테이블 형식)
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"

# 기존 UserAdmin을 커스터마이징해서 ProfileInline 추가
class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

# 기존 UserAdmin을 새로운 CustomUserAdmin으로 덮어쓰기
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
