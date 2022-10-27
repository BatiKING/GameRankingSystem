from django.shortcuts import render, redirect
from django.views import View
from Game_Ranking_System.models import Score, User, GameMode, GameTitle
from django.contrib.auth.views import LoginView
from Game_Ranking_System.forms.forms import LoginForm, SignUpForm, AddPublicMatchForm, AddPersonalMatchForm, \
    AddPublicMatchSelectGameForm
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate


# Create your views here.
class LandingView(View):
    def get(self, request):
        # new_score = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=10, p2_score=3, p1_character='Czong',
        #                                  p2_character='Chuj')
        # PublicScore.objects.create(score=new_score, game_title_id_id=1, game_mode_id_id=1, creator_id_id=1,
        #                            opponent_id_id=2, score_confirmed=True)

        public_scores = Score.objects.filter(public_score=True).filter(score_confirmed=True)

        ctx = {
            'matches': public_scores,
            'board_type': "Public Score board"
        }
        return render(request, "score_board.html", ctx)


class PersonalScoreView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("home")

        personal_score = Score.objects.filter(p1_id__username=request.user.username) | Score.objects.filter(
            p2_id__username=request.user.username)
        personal_score = personal_score.filter(public_score=False)

        ctx = {
            'matches': personal_score,
            'board_type': "Personal Score board"
        }

        return render(request, "score_board.html", ctx)


class UserLoginView(LoginView):
    def get(self, request):
        logout(request)
        LoginView.template_name = 'LoginView_form.html'
        ctx = {'form': LoginForm()}
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


class AddPublicMatchView(View):

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("home")

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
                match_result_object.score_confirmed = True  # temporary
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

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("home")

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
