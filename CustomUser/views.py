from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms  import UserSignUpForm,LoginForm
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from ContestantPost.models import Contest,Post,Vote,storeVote
from django.db.models import Max
# Create your views here.

def HomePage(request):
    return render(request,'home.html')

def signin(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        user=authenticate(email=email,password=password)
        if user is not None:
            login(request,user)
            if user.isContestant:
                return redirect('cdashboard')
            elif user.isVoter:
                return redirect('vdashboard')
            logout(request)
            messages.add_message(request,messages.ERROR,"login with contestant or voter id ")
            return redirect('signin')
        messages.add_message(request,messages.ERROR,"email or password doesn't match!!")
    context={
        'form':form
    }

    return render(request,'signin.html',context)

def signout(request):
    logout(request)
    return redirect('signin')
def about(request):
    return render(request,'about.html')

def signUpContestant(request):
    if request.method=='POST':
        form=UserSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(False)
            if user.contact.isdigit():
                user.isContestant=True
                user.isVoter=False
                user.set_password(request.POST['password'])
                user.save(True)
                messages.add_message(request,messages.SUCCESS,"signUP successfull")
                return redirect('signin')

            messages.add_message(request,messages.ERROR,"contact should be of all digit!!!")
            return redirect('signupcontestant')
    else:
        form=UserSignUpForm()
    context={
        'form':form
    }
    return render(request,'contestant/signup.html',context)

def signUpVoter(request):
    if request.method=='POST':
        form=UserSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save(False)
            if user.contact.isdigit():
                user.isVoter=True
                user.isContestant=False
                user.set_password(request.POST['password'])
                user.save(True)
                messages.add_message(request,messages.SUCCESS,"signUP successfull")
                return redirect('signin')

            messages.add_message(request,messages.ERROR,"contact should be of all digit!!!")
            return redirect('signupvoter')
            
    form=UserSignUpForm()
    context={
        'form':form
    }
    return render(request,'voter/signup.html',context)

@login_required(login_url='signin')
def ContestantDashboard(request):
    contests=Contest.objects.all()
    if request.user.isContestant:
        context={
            'user':request.user,
            'contests':contests
        }
        return render(request,'contestant/dashboard.html',context)
    return redirect('vdashboard')

@login_required(login_url='signin')
def VoterDashboard(request):
    contests = Contest.objects.all()
    if request.user.isVoter:
        context = {
            'user': request.user,
            'contests': contests
        }
        return render(request,'voter/dashboard.html',context)
    return redirect('cdashboard')

@login_required(login_url='signin')
def ContestantListForVoter(request,id):
    voted=False
    vtab=Vote.objects.all()
    for v in vtab:
        if request.user.id==v.user.id and id==v.contest.id:
            voted=True
            break
    try:
        if request.user.isVoter:
            posts = Post.objects.filter(contest_id=id).filter(contestant__is_active=True)
            print(posts)
            context = {
                    'posts': posts,
                    'user':request.user,
                    'cid':id,
                    'voted':voted
            }
            return render(request,'voter/contestantlistforVoter.html', context)
        return HttpResponse("not voter")
    except Exception as e:
        messages.add_message(request, messages.ERROR, e)
        return redirect('vdashboard')

def ChangeProfile(request,id):
    u = get_object_or_404(User,id=id)
    form = UserSignUpForm(request.POST or None, request.FILES or None,instance=u)
    if u.isVoter:
        if request.method == 'POST':
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                address=form.cleaned_data['address']
                contact=form.cleaned_data['contact']
                password=form.cleaned_data['password']
                image=form.cleaned_data['image']
                gender=form.cleaned_data['gender']
                try:
                    user=User(id=id,username=username,email=email,address=address,contact=contact,password=password,image=image,gender=gender)
                    user.set_password(password)
                    user.isVoter=True
                    user.isContestant = False
                    update_session_auth_hash(request, user)
                    user.save()
                    messages.success(request,'profile changed successfully')
                    return redirect('vdashboard')
                except Exception as e:
                    messages.error(request,e)
                    return redirect('vdashboard')
    else:
        if request.method == 'POST':
            if form.is_valid():
                username=form.cleaned_data['username']
                email=form.cleaned_data['email']
                address=form.cleaned_data['address']
                contact=form.cleaned_data['contact']
                password=form.cleaned_data['password']
                image=form.cleaned_data['image']
                gender=form.cleaned_data['gender']
                try:
                    user=User(id=id,username=username,email=email,address=address,contact=contact,password=password,image=image,gender=gender)
                    user.set_password(password)
                    user.isVoter=False
                    user.isContestant=True
                    update_session_auth_hash(request, u)
                    user.save()
                    messages.success(request,'profile changed successfully')
                    return redirect('cdashboard')
                except Exception as e:
                    messages.error(request,e)
                    return redirect('cdashboard')
    context = {
        'form': form,
        'uid':id
    }
    return render(request,'changeProfile.html', context)

# def DeleteUser(request,id):
#     user = get_object_or_404(User, id=id)
#     votes=Vote.objects.filter(user_id=id)
#     storevote=storeVote.objects.filter(voter=id)
#     storevote.delete()
#     votes.delete()
#     user.delete()
#     messages.success(request,'user deleted successfully and vote is reduced from respective contestents also')
#     return redirect('home')


# from ContestantPost.models import Vote as V
def Voting(request,cid,id):
    try:
        user=User.objects.get(id=request.user.id)
        v = Vote(user=user,contest_id=cid,contestant=id)
        v.save()
        votes=Vote.objects.filter(contest_id=cid).filter(contestant=id).count()
        print(votes)
        convote=storeVote(contest_id=cid,contestant_id=id,vote=votes,voter=request.user.id)
        convote.save()
        messages.add_message(request,messages.SUCCESS,"thanks for voting")
        return redirect('vdashboard')
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
        return redirect('vdashboard')

def saveVote(request,cid):
    winner=storeVote.objects.filter(contest_id=cid)
    max=winner.aggregate(Max('vote'))
    winners=storeVote.objects.filter(vote=max['vote__max']).filter(contestant__is_active=True).filter(contest_id=cid)
    context={
        'winners':winners
    }
    return render(request,'winner.html',context)
    
    





