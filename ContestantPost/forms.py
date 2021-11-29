from django import forms
from .models import Post



class CreatePostForm(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'write cool caption','id':'title'}))

    class Meta:
        model= Post
        fields =( 'title','image')

    def save(self,commit=True):
        post=super(CreatePostForm,self).save(commit=commit)
        if commit:
            post.save()
        return post