from django.urls import path
from .views import (
    index,
    login_view,
    signup_view,
    logout_view,
    apply_club,
    check_result,
    admin_home,
    admin_club_applicants,
    admin_update_status,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('register/', apply_club, name='apply_club'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('check/', check_result, name='check'),
    path('logout/', logout_view, name='logout'),
    # 관리자 사이트 URL
    path('adminsite/', admin_home, name='admin_home'),
    path('adminsite/<str:club_name>/', admin_club_applicants, name='admin_club_applicants'),
    path('adminsite/<str:club_name>/update/', admin_update_status, name='admin_update_status'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
