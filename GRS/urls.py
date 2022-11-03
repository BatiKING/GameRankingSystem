"""GRS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Game_Ranking_System.views import LandingView, UserLoginView, SignupView, PersonalScoreView, AddPublicMatchView, \
    AddPersonalMatchView, RankingView, ConfirmScoreView, ScoreRequestDeleteView, ScoreRequestConfirmView
from django.contrib.auth import views as auth_views
from Game_Ranking_System.forms.forms import LoginForm
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LandingView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(authentication_form=LoginForm), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('personal/', login_required(PersonalScoreView.as_view()), name='personal'),
    path('add_public/', login_required(AddPublicMatchView.as_view()), name='add_public'),
    path('add_personal/', login_required(AddPersonalMatchView.as_view()), name='add_personal'),
    path('ranking/', login_required(RankingView.as_view()), name='ranking'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('confirm_score/', login_required(ConfirmScoreView.as_view()), name='confirm_score'),
    path('delete_score_request/<int:match_id>', login_required(ScoreRequestDeleteView.as_view()),
         name='delete_score_request'),
    path('confirm_score_request/<int:match_id>', login_required(ScoreRequestConfirmView.as_view()),
         name='confirm_score_request'),

]
