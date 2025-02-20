from django.db import models

# Create your models here.
from django.db import models

class Club(models.Model):
    CLUB_TYPES = [
        ('제1동아리', '제1동아리'),
        ('제2동아리', '제2동아리'),
        ('자율동아리', '자율동아리'),
    ]

    name = models.CharField(max_length=100, unique=True)  # 동아리 이름
    club_type = models.CharField(max_length=20, choices=CLUB_TYPES)  # 동아리 유형
    subject = models.CharField(max_length=100, default='')  # 동아리 과목
    description = models.TextField()  # 동아리 설명
    leader = models.CharField(max_length=50)  # 기장 이름
    poster = models.ImageField(upload_to='club_posters/')  # 동아리 포스터 이미지

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True, verbose_name="학번")
    is_leader = models.BooleanField(default=False, verbose_name="기장 여부")

    # 동아리 지원 정보
    first_choice_club1 = models.CharField(max_length=100, blank=True, null=True, verbose_name="1지망 제1동아리")
    first_choice_club1_status = models.CharField(
        max_length=10, choices=[("true", "합격"), ("false", "불합격"), ("none", "미정")], default="none"
    )

    second_choice_club1 = models.CharField(max_length=100, blank=True, null=True, verbose_name="2지망 제1동아리")
    second_choice_club1_status = models.CharField(
        max_length=10, choices=[("true", "합격"), ("false", "불합격"), ("none", "미정")], default="none"
    )

    first_choice_club2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="1지망 제2동아리")
    first_choice_club2_status = models.CharField(
        max_length=10, choices=[("true", "합격"), ("false", "불합격"), ("none", "미정")], default="none"
    )

    second_choice_club2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="2지망 제2동아리")
    second_choice_club2_status = models.CharField(
        max_length=10, choices=[("true", "합격"), ("false", "불합격"), ("none", "미정")], default="none"
    )

    def __str__(self):
        return f"{self.user.username} ({self.student_id})"