from django.contrib import admin
from django.urls import path
from . import views
from ContestantPost.views import CreatePost,contestantList
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.HomePage,name='home'),
    path('signup/contestant/',views.signUpContestant,name='signupcontestant'),
    path('signup/voter/',views.signUpVoter,name='signupvoter'),
    path('signin/',views.signin,name='signin'),
    path('aboutus/',views.about,name='aboutus'),
    path('contestant/dashboard/',views.ContestantDashboard,name='cdashboard'),
    path('voter/dashboard/',views.VoterDashboard,name='vdashboard'),
    path('logout/',views.signout,name='logout'),
    path('contestant/dashboard/createpost/<int:id>',CreatePost,name='createpost'),
    path('contestant/dashboard/contestantlist/<int:id>',contestantList,name='contestantlist'),
    path('voter/dashboard/contestantlist/<int:id>',views.ContestantListForVoter,name='contestantlistforvoter'),
    path('voter/dashboard/contestantlist/vote/<int:cid>/<int:id>',views.Voting,name='vote'),
    path('user/dashboard/changeProfile/<int:id>',views.ChangeProfile,name='changeprofile'),
    # path('user/dashboard/delete/<int:id>',views.DeleteUser,name='deleteUser'),
    path('winner/<int:cid>',views.saveVote,name='winner'),

    # password reset urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
