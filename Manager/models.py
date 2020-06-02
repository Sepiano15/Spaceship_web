from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class myuser(AbstractUser):
	score_one = models.IntegerField("운석 피하기 점수",default=0)
	score_two = models.IntegerField("핑퐁 점수",default=0)
	score_three = models.IntegerField("텐가이 점수",default=0)
	rank_one = models.IntegerField("운석 피하기 순위",default=0)
	rank_two = models.IntegerField("핑퐁 순위",default=0)
	rank_three = models.IntegerField("텐가이 순위",default=0)
	ranker = models.BooleanField(default=False)