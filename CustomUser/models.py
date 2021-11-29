from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

gender= (('male','MALE'),('female','FEMALE'),('other','OTHER'))

# Create your models here.
class UserManager(BaseUserManager):
      def create_user(self,email,username,address,password=None):
            user=self.model(
                  email=self.normalize_email(email),
                  username=username,
                  address=address
                  )
            user.set_password(password)
            user.save(using=self._db)
            return user
      def create_superuser(self,email,username,address,password=None):
            user=self.create_user(email,username,address,password)
            user.is_admin=True
            user.save(using=self._db)
            return user
class User(AbstractBaseUser):
      username=models.CharField(max_length=100)
      email=models.EmailField(unique=True,verbose_name="Email")
      contact=models.CharField(blank=True,null=True,max_length=100)
      address=models.CharField(max_length=100)
      image=models.ImageField(upload_to="users/",default="")
      gender=models.CharField(max_length=6,choices=gender,default=gender[0][0])
      isContestant=models.BooleanField(default=False)
      isVoter=models.BooleanField(default=False)
      is_active=models.BooleanField(default=True)
      is_admin=models.BooleanField(default=False)
      objects = UserManager()
      USERNAME_FIELD='email'
      REQUIRED_FIELDS=['username','address']

      def __str__(self):
            return self.username
      def has_perm(self,perm,obj=None):
            return True
      def has_module_perms(self,app_label):
            return True
      @property
      def is_staff(self):
            return self.is_admin