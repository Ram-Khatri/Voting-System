from django import forms
from .models import User
from django.utils import timezone



class UserSignUpForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter username','class':'form-control','id':'uname'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter email','class':'form-control','id':'email'}))
    contact=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter contact','class':'form-control','id':'contact','max':10}))
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter address','class':'form-control','id':'address'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'form-control','id':'pass1'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'form-control','id':'pass2'}),label='Confirm password')

    class Meta:
        model= User
        fields=['username','email','contact','address','image','gender','password','password2']

    def clean(self):
        cleaned_data= super(UserSignUpForm,self).clean()
        password=cleaned_data.get('password')
        password2= cleaned_data.get('password2')
        if password != password2:
            self.add_error('password2','enter same password!!')
        return cleaned_data

    def save(self,commit=True):
        user=super(UserSignUpForm,self).save(commit=commit)
        user.last_login=timezone.now()
        if commit:
            user.save()
        return user
class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter email','class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password','class':'form-control'}))




