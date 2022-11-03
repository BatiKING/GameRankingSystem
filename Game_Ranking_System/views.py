from django.shortcuts import render, redirect
from django.views import View
from Game_Ranking_System.models import Score, User, GameMode, GameTitle
from django.contrib.auth.views import LoginView
from Game_Ranking_System.forms.forms import LoginForm, SignUpForm, AddPublicMatchForm, AddPersonalMatchForm, \
    AddPublicMatchSelectGameForm, ScoreFilter, RankingFilter
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from django.db.models import F, Case, When, Value, Count, IntegerField, Sum
from django.db.models.functions import Abs


# Create your views here.
class LandingView(View):
    """View dedicated for the landing page, it displays login / signup buttons, or nav menu for logged-in users,
    it also displays Public score board for all users"""

    def get(self, request):
        public_scores = Score.objects.filter(public_score=True).filter(score_confirmed=True)
        public_scores = public_scores.order_by('-date_time_created')
        public_scores = public_scores.annotate(
            score_dif=Abs(F('p1_score') - F('p2_score')))
        score_filter = ScoreFilter(request.GET, queryset=public_scores)
        score_filter.filters['game_title_id'].field.queryset = score_filter.filters[
            'game_title_id'].field.queryset.filter(
            public_allowed=True)
        public_scores = score_filter.qs
        # public_scores = public_scores.order_by('-date_time_created')
        # public_scores = public_scores.annotate(
        #     score_dif=Abs(F('p1_score') - F('p2_score'))).order_by('-score_dif')
        ctx = {
            'matches': public_scores,
            'board_type': "Public Score board",
            'score_filter': score_filter
        }
        return render(request, "score_board.html", ctx)


class PersonalScoreView(View):
    """View dedicated for Personal Score board, visible only to logged-in users"""

    def get(self, request):
        # if not request.user.is_authenticated:
        #     return redirect("home")

        personal_score = Score.objects.filter(p1_id__username=request.user.username) | Score.objects.filter(
            p2_id__username=request.user.username)
        personal_score = personal_score.filter(public_score=False)
        personal_score = personal_score.order_by('-date_time_created')
        personal_score = personal_score.annotate(
            score_dif=Abs(F('p1_score') - F('p2_score')))
        score_filter = ScoreFilter(request.GET, queryset=personal_score)
        personal_score = score_filter.qs
        ctx = {
            'matches': personal_score,
            'board_type': "Personal Score board",
            'score_filter': score_filter
        }

        return render(request, "score_board.html", ctx)


class UserLoginView(LoginView):
    """Log in View"""

    def get(self, request):
        logout(request)
        LoginView.template_name = 'LoginView_form.html'
        ctx = {'form': LoginForm()}
        return render(request, "LoginView_form.html", ctx)


class SignupView(View):
    """Signup view"""

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


class AddPublicMatchView(View):
    """View dedicated for Add Public Score page, visible only to logged-in users"""

    def post(self, request):
        # if not request.user.is_authenticated:
        #     return redirect("home")

        if request.POST.get('add_public_game_title_id'):
            request.session['add_public_game_title_id'] = request.POST.get('add_public_game_title_id')
            form = AddPublicMatchForm(request.user, request.session['add_public_game_title_id'])
            print(f"add public game title = {request.session['add_public_game_title_id']}")
            ctx = {'form': form, 'match_type': "public"}
            return render(request, 'add_match.html', ctx)

        if request.session.get('add_public_game_title_id'):
            form = AddPublicMatchForm(request.user, request.session['add_public_game_title_id'], request.POST)

            if form.is_valid():
                match_result_object = form.save(commit=False)
                match_result_object.p1_id = User.objects.get(pk=request.user.id)
                match_result_object.public_score = True
                # match_result_object.score_confirmed = True  # temporary
                match_result_object.save()
                return redirect('home')
            else:
                ctx = {"add_match_error": form.errors, 'form': AddPublicMatchForm(current_user=request.user,
                                                                                  game_title_id=request.session[
                                                                                      'add_public_game_title_id']),
                       'match_type': "public"}
                return render(request, 'add_match.html', ctx)
        else:
            form = AddPublicMatchSelectGameForm()
            ctx = {'form': form, 'match_type': "public"}
            return render(request, 'add_match.html', ctx)

        form = AddPublicMatchSelectGameForm()
        ctx = {'form': form, 'match_type': 'public'}
        return render(request, 'add_match.html', ctx)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("home")

        # form = AddPublicMatchForm(current_user=request.user)
        # ctx = {'form': form, 'match_type': "public"}
        # return render(request, 'add_match.html', ctx)

        if request.POST.get('add_public_game_title_id'):
            form = AddPublicMatchForm(current_user=request.user,
                                      game_title_id=request.session['add_public_game_title_id'])
            ctx = {'form': form, 'match_type': "public"}
            return render(request, 'add_match.html', ctx)
        else:
            form = AddPublicMatchSelectGameForm()
            ctx = {'form': form, 'match_type': "public"}
            return render(request, 'add_match.html', ctx)


class AddPersonalMatchView(View):
    """View dedicated for Add Personal Score page, visible only to logged-in users"""

    def post(self, request):
        # if not request.user.is_authenticated:
        #     return redirect("home")

        copy_POST = request.POST.copy()
        # check if Game title and Game mode exist already and create them if they don't
        if GameMode.objects.filter(mode=copy_POST['game_mode_id']).first():
            copy_POST['game_mode_id'] = GameMode.objects.get(mode=copy_POST['game_mode_id'])
        else:
            copy_POST['game_mode_id'] = GameMode.objects.create(mode=copy_POST['game_mode_id'])

        if GameTitle.objects.filter(title=copy_POST['game_title_id']).first():
            copy_POST['game_title_id'] = GameTitle.objects.get(title=copy_POST['game_title_id'])
        else:
            copy_POST['game_title_id'] = GameTitle.objects.create(title=copy_POST['game_title_id'])

        form = AddPersonalMatchForm(copy_POST)
        if form.is_valid():
            match_result_object = form.save(commit=False)
            match_result_object.p1_id = User.objects.get(pk=request.user.id)
            match_result_object.public_score = False
            match_result_object.score_confirmed = True
            match_result_object.save()
            return redirect('home')
        else:
            ctx = {"add_match_error": form.errors, 'form': AddPersonalMatchForm(), 'match_type': "personal"}
            return render(request, 'add_match.html', ctx)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("home")
        form = AddPersonalMatchForm()
        ctx = {'form': form, 'match_type': "personal"}
        return render(request, 'add_match.html', ctx)


class RankingView(View):
    """View dedicated for Ranking page, visible only to logged-in users.
    Aggregates and sorts data from Score model in order to project a ranking."""

    def get(self, request):
        # if not request.user.is_authenticated:
        #     return redirect("home")

        ranking = Score.objects.filter(public_score=True).filter(score_confirmed=True)

        ranking = ranking.annotate(
            p1_win=Case(
                When(p1_score__gt=F('p2_score'), then=1),
                output_field=IntegerField(), default=0
            ))

        score_filter = RankingFilter(request.GET, queryset=ranking)
        ranking = score_filter.qs

        ranking_data = {}
        for match in ranking:
            if match.p1_id.nickname not in ranking_data:
                ranking_data[match.p1_id.nickname] = {'wins': 0, 'matches_played': 1}
            else:
                ranking_data[match.p1_id.nickname]['matches_played'] += 1

            if match.p2_id.nickname not in ranking_data:
                ranking_data[match.p2_id.nickname] = {'wins': 0, 'matches_played': 1}
            else:
                ranking_data[match.p2_id.nickname]['matches_played'] += 1

            if match.p1_win:
                ranking_data[match.p1_id.nickname]['wins'] += 1
            else:
                ranking_data[match.p2_id.nickname]['wins'] += 1
        order_list = [(values['wins'], nick) for nick, values in ranking_data.items() if values['wins'] > 0]

        order_list.sort(reverse=True)
        sorted_ranking_data = {nick[1]: ranking_data[nick[1]] for nick in order_list}
        print(sorted_ranking_data)
        ranking_data = sorted_ranking_data
        for i, key in enumerate(ranking_data.keys()):
            if i == 0:
                ranking_data[key]['rank'] = 1
            else:
                if ranking_data[key]['wins'] == ranking_data[list(ranking_data.keys())[i - 1]]['wins']:
                    ranking_data[key]['rank'] = ranking_data[list(ranking_data.keys())[i - 1]]['rank']
                else:
                    # ranking_data[key]['rank'] = ranking_data[list(ranking_data.keys())[i - 1]]['rank']+1
                    ranking_data[key]['rank'] = i + 1
        sort_game = ''
        if score_filter.form.cleaned_data['game_title_id']:
            sort_game = f": {score_filter.form.cleaned_data['game_title_id']}"

        ctx = {
            'matches': ranking,
            'board_type': f"Ranking{sort_game}",
            'score_filter': score_filter,
            'ranking_data': ranking_data
        }
        return render(request, "ranking.html", ctx)


class ConfirmScoreView(View):
    """View used to allow user confirm or reject a pending public match result submitted by another user"""

    def get(self, request):
        matches = Score.objects.filter(public_score=True).filter(p2_id=request.user.id).filter(score_confirmed=False)

        score_filter = RankingFilter(request.GET, queryset=matches)
        matches = score_filter.qs

        if score_filter.form.cleaned_data['game_title_id']:
            sort_game = f": {score_filter.form.cleaned_data['game_title_id']}"

        ctx = {
            'matches': matches,
            'score_filter': score_filter,
        }
        return render(request, "confirm_score.html", ctx)


class ScoreRequestDeleteView(View):
    """No-template view, only meant to delete a rejected public score when user press 'Delete' button"""

    def get(self, request, match_id):
        score_to_delete = Score.objects.filter(pk=match_id).filter(p2_id=request.user.id).filter(
            score_confirmed=False).filter(public_score=True).first()
        if score_to_delete:
            score_to_delete.delete()
            return redirect('confirm_score')
        else:
            return redirect('confirm_score')


class ScoreRequestConfirmView(View):
    """No-template view, only meant to confirm a valid public score when user press 'Confirm' button"""

    def get(self, request, match_id):
        score_to_confirm = Score.objects.filter(pk=match_id).filter(p2_id=request.user.id).filter(
            score_confirmed=False).filter(public_score=True).first()
        if score_to_confirm:
            score_to_confirm.score_confirmed = True
            score_to_confirm.save()
            return redirect('confirm_score')
        else:
            return redirect('confirm_score')
