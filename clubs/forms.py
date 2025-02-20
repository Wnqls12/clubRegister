from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    # User 모델에 없는 추가 필드는 여기서 따로 입력받고, 저장 시 Profile에 저장합니다.
    name = forms.CharField(max_length=30, required=True, label="이름")
    student_id = forms.CharField(max_length=10, required=True, label="학번")

    class Meta:
        model = User
        # User 모델의 기본 필드: username, password1, password2
        fields = ("username", "name", "student_id", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        # 이름은 User 모델의 first_name 필드에 저장 (원하는 대로 커스터마이징 가능)
        user.first_name = self.cleaned_data["name"]
        if commit:
            user.save()
            # 회원가입 시 Profile 생성
            Profile.objects.create(user=user, student_id=self.cleaned_data["student_id"])
        return user


from django import forms
from .models import Club

class ClubApplicationForm(forms.Form):
    club1_1 = forms.ChoiceField(label="1지망 제1 동아리 선택", choices=[])
    club1_2 = forms.ChoiceField(label="2지망 제1 동아리 선택", choices=[])
    club2_1 = forms.ChoiceField(label="1지망 제2 동아리 선택", choices=[])
    club2_2 = forms.ChoiceField(label="2지망 제2 동아리 선택", choices=[])
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호 입력")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 제1 동아리 목록 (Club.club_type == "제1동아리")
        club1_qs = Club.objects.filter(club_type="제1동아리")
        # 제2 동아리 목록 (Club.club_type == "제2동아리")
        club2_qs = Club.objects.filter(club_type="제2동아리")
        self.fields['club1_1'].choices = [("", "동아리를 선택해주세요")] + [(club.name, club.name) for club in club1_qs]
        # 2지망은 '없음' 옵션 추가
        self.fields['club1_2'].choices = [("", "동아리를 선택해주세요")] + [(club.name, club.name) for club in club1_qs] + [("없음", "없음")]
        self.fields['club2_1'].choices = [("", "동아리를 선택하세요")] + [(club.name, club.name) for club in club2_qs]
        self.fields['club2_2'].choices = [("", "동아리를 선택하세요")] + [(club.name, club.name) for club in club2_qs] + [("없음", "없음")]
