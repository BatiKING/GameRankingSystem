from django.shortcuts import render
from django.views import View
from Game_Ranking_System.models import Score, PublicScore, User
from django.contrib.auth.views import LoginView
from Game_Ranking_System.forms.forms import LoginForm

# Create your views here.
class LandingView(View):
    def get(self, request):
        # new_score = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=10, p2_score=3, p1_character='Czong',
        #                                  p2_character='Chuj')
        # PublicScore.objects.create(score=new_score, game_title_id_id=1, game_mode_id_id=1, creator_id_id=1,
        #                            opponent_id_id=2, score_confirmed=True)

        public_scores = PublicScore.objects.all()

        ctx = {
            'matches': public_scores
        }
        return render(request, "index.html", ctx)


class UserLoginView(LoginView):
    def get(self, request):

        ctx = {}
        ctx['form'] = LoginForm()
        return render(request, "LoginView_form.html", ctx)
