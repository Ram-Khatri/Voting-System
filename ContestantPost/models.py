from django.db import models
from CustomUser.models import User


# Create your models here.
class Contest(models.Model):
    name=models.CharField(max_length=50)
    contest_type=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='contest/')
    startdate=models.DateField()
    end_date=models.DateField()
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='contestantPost/')
    contestant=models.ForeignKey(User,on_delete=models.CASCADE)
    contest=models.ForeignKey(Contest,on_delete=models.CASCADE)
    posted_date=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.contestant.username

    class Meta:
        unique_together=('contest','contestant')

class Vote(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    contest=models.ForeignKey(Contest,on_delete=models.CASCADE)
    contestant = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together=('user','contest','contestant')

class storeVote(models.Model):
    contestant=models.ForeignKey(User,on_delete=models.CASCADE)
    contest=models.ForeignKey(Contest,on_delete=models.CASCADE)
    vote=models.IntegerField(default=0)
    voter=models.IntegerField(default=0)

    def __str__(self):
        return self.contestant.username


