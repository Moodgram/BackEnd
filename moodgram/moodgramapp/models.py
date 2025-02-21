from django.db import models
from django.contrib.auth.models import AbstractUser

# 사용자(User) 모델 (Django 기본 User 확장)
class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100, unique=True)
    profile_image = models.TextField(blank=True, null=True)
    
    groups = models.ManyToManyField(
        "auth.Group",
        related_name= "moodgram_users",
        blank = True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="moodgram_users_permissions",
        blank=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.nickname


# 일기(Diary) 모델
class Diary(models.Model):
    MOOD_CHOICES = [
        ('happy', '행복'),
        ('sad', '슬픔'),
        ('neutral', '중립'),
        ('angry', '화남'),
        ('excited', '신남'),
    ]

    WEATHER_CHOICES = [
        ('sunny', '맑음'),
        ('cloudy', '흐림'),
        ('rainy', '비'),
        ('snowy', '눈'),
        ('stormy', '폭풍'),
        ('foggy', '안개'),
        ('windy', '바람'),
        ('hazy', '미세먼지'),
    ]

    VISIBILITY_CHOICES = [
        ('public', '공개'),
        ('private', '비공개'),
        ('friends-only', '친구공개'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    weather = models.CharField(max_length=20, choices=WEATHER_CHOICES, null=False)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, null=False)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname} - {self.title or 'No Title'}"


# 일기 이미지 모델
class DiaryImage(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='images')
    image_url = models.TextField()

    def __str__(self):
        return f"Image for {self.diary}"


# 댓글(Comment) 모델
class Comment(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.nickname if self.user else 'Unknown'} on {self.diary}"


# 좋아요(Like) 모델
class Like(models.Model):
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('diary', 'user')

    def __str__(self):
        return f"{self.user.nickname if self.user else 'Unknown'} liked {self.diary}"


# 친구 관계(Friendship) 모델
class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('accepted', '수락됨'),
        ('rejected', '거절됨'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.nickname} -> {self.friend.nickname} ({self.status})"


# AI 감정 분석(AIAnalysis) 모델
class AIAnalysis(models.Model):
    diary = models.OneToOneField(Diary, on_delete=models.CASCADE, related_name='ai_analysis')
    mood = models.CharField(max_length=10, choices=Diary.MOOD_CHOICES)
    ai_suggestion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"AI Analysis for {self.diary}"
