from django.shortcuts import render, redirect
from django.views import View
from Game_Ranking_System.models import Score, User
from django.contrib.auth.views import LoginView
from Game_Ranking_System.forms.forms import LoginForm, SignUpForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate


# Create your views here.
class LandingView(View):
    def get(self, request):
        # new_score = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=10, p2_score=3, p1_character='Czong',
        #                                  p2_character='Chuj')
        # PublicScore.objects.create(score=new_score, game_title_id_id=1, game_mode_id_id=1, creator_id_id=1,
        #                            opponent_id_id=2, score_confirmed=True)

        public_scores = Score.objects.all()

        ctx = {
            'matches': public_scores
        }
        return render(request, "index.html", ctx)


class UserLoginView(LoginView):
    def get(self, request):
        logout(request)
        LoginView.template_name = 'LoginView_form.html'
        ctx = {}
        ctx['form'] = LoginForm()
        return render(request, "LoginView_form.html", ctx)


class SignupView(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            ctx = {"signup_error": form.errors, 'form': SignUpForm()}
            return render(request, "signup.html", ctx)

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
