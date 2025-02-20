from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import ClubApplicationForm
from .forms import SignupForm  # 기존 회원가입 폼(이미 구현된 것으로 가정)
from .models import Profile, Club
from django.contrib.auth.models import User

def index(request):
    from .models import Club
    clubs = Club.objects.all()
    return render(request, 'index.html', {'clubs': clubs})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 회원가입 후 바로 로그인
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('index')


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ClubApplicationForm


@login_required
def apply_club(request):
    profile = request.user.profile


    if request.method == "POST":
        form = ClubApplicationForm(request.POST)
        if form.is_valid():
            # 비밀번호 확인은 form에서 처리했으므로, 여기서는 바로 저장
            profile.first_choice_club1 = form.cleaned_data["club1_1"]
            profile.second_choice_club1 = form.cleaned_data["club1_2"]
            profile.first_choice_club2 = form.cleaned_data["club2_1"]
            profile.second_choice_club2 = form.cleaned_data["club2_2"]
            # 신청 시 합격 상태를 모두 "none" (미정)으로 초기화
            profile.first_choice_club1_status = "none"
            profile.second_choice_club1_status = "none"
            profile.first_choice_club2_status = "none"
            profile.second_choice_club2_status = "none"
            profile.save()
            messages.success(request, "동아리 신청이 완료되었습니다!")
            return redirect("index")
    else:
        form = ClubApplicationForm()
    return render(request, "register.html", {"form": form})


@login_required
def check_result(request):
    profile = request.user.profile
    context = {
       "club1_1": profile.first_choice_club1,
       "result1_1": profile.first_choice_club1_status,
       "club1_2": profile.second_choice_club1,
       "result1_2": profile.second_choice_club1_status,
       "club2_1": profile.first_choice_club2,
       "result2_1": profile.first_choice_club2_status,
       "club2_2": profile.second_choice_club2,
       "result2_2": profile.second_choice_club2_status,
    }
    print(context)
    return render(request, "check.html", context)


from django.core.exceptions import PermissionDenied

def leader_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.profile.is_leader:
            raise PermissionDenied("관리자 권한이 필요합니다.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

from .models import Club

@leader_required
def admin_home(request):
    clubs = Club.objects.all()
    return render(request, "admin_home.html", {"clubs": clubs})


from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

@leader_required
def admin_club_applicants(request, club_name):
    applications = []
    for profile in Profile.objects.all():
        if profile.first_choice_club1 == club_name:
            applications.append({
                "profile": profile,
                "field": "first_choice_club1",
                "status": profile.first_choice_club1_status,  # "true", "false", "none"
            })
        if profile.second_choice_club1 == club_name:
            applications.append({
                "profile": profile,
                "field": "second_choice_club1",
                "status": profile.second_choice_club1_status,
            })
        if profile.first_choice_club2 == club_name:
            applications.append({
                "profile": profile,
                "field": "first_choice_club2",
                "status": profile.first_choice_club2_status,
            })
        if profile.second_choice_club2 == club_name:
            applications.append({
                "profile": profile,
                "field": "second_choice_club2",
                "status": profile.second_choice_club2_status,
            })
    context = {
        "club_name": club_name,
        "applications": applications,
    }
    return render(request, "admin_club_applicants.html", context)


@leader_required
@require_POST
def admin_update_status(request, club_name):
    for key, value in request.POST.items():
        if "__" in key:
            try:
                profile_id, field_status = key.split("__", 1)
                profile = Profile.objects.get(id=profile_id)
                if field_status in ["first_choice_club1_status", "second_choice_club1_status",
                                    "first_choice_club2_status", "second_choice_club2_status"]:
                    setattr(profile, field_status, value)
                    profile.save()
            except Exception as e:
                continue
    messages.success(request, "저장되었습니다.")
    return HttpResponseRedirect(reverse("admin_club_applicants", args=[club_name]))
