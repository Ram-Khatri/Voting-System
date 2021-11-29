from django.shortcuts import render,redirect
from .forms import CreatePostForm
from .models import Post,Contest
from django.contrib import messages
from CustomUser.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='signin')
def CreatePost(request,id):
    if request.user.isContestant:
        form=CreatePostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post=form.save(False)
            if request.user.is_active:
                post.contestant_id=request.user.id
                post.contest_id=id
                try:
                    post.save(True)
                    messages.add_message(request,messages.SUCCESS,"posted successfully")
                    return redirect('cdashboard')
                except Exception:
                    messages.add_message(request,messages.ERROR,"You are already posted")
                    return redirect('cdashboard')
            messages.add_message(request,messages.ERROR,"Sorry you are Deactivated by admin")
            return redirect('cdashboard')

        context={
            'form':form,
            'contest_id':id
        }
        return render(request,'contestant/contestantPost.html',context)

@login_required(login_url='signin')
def contestantList(request,id):
    try:
        posts=Post.objects.filter(contest_id=id).filter(contestant__is_active=True)
        if request.user.isContestant:
            context={
                'user':request.user,
                'posts':posts
            }
            return render(request,'contestant/contestantList.html',context)
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
        return redirect('cdashboard')

