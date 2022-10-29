from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Game_Ranking_System.models import User, Score, GameMode, GameTitle
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation, )
import django_filters
from django_filters import CharFilter


class ScoreFilter(django_filters.FilterSet):

    player_nickname = CharFilter(method='custom_filter_both_nicknames', label='Nickname',
                                 widget=forms.widgets.TextInput(attrs={'class': 'form-control-sm'}))
    character = CharFilter(method='custom_filter_both_characters', label='Character',
                           widget=forms.widgets.TextInput(attrs={'class': 'form-control-sm'}))

    sort_filter = django_filters.OrderingFilter(
        fields=['date_time_created', 'score_dif'],
        field_labels={'date_time_created': 'Date added', 'score_dif': "Score difference"},
        label='Sort',

    )


    def __init__(self, *args, **kwargs):
        super(ScoreFilter, self).__init__(*args, **kwargs)
        self.filters['game_title_id'].label = "Game"
        self.filters['game_title_id'].field.widget.attrs.update(
            {'class': 'form-select-sm'})
        self.filters['sort_filter'].field.widget.attrs['class'] = 'form-select-sm'


    class Meta:
        model = Score
        fields = ['game_title_id']

    def custom_filter_both_nicknames(self, queryset, name, value):
        qs1 = queryset.filter(p1_id__nickname__icontains=value)
        qs2 = queryset.filter(p2_id__nickname__icontains=value)
        return qs1 | qs2

    def custom_filter_both_characters(self, queryset, name, value):
        qs1 = queryset.filter(p1_character__icontains=value)
        qs2 = queryset.filter(p2_character__icontains=value)
        return qs1 | qs2


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control'}
        )
    # username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    # password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs["class"] = "form-control"
        self.fields['password2'].widget.attrs["class"] = "form-control"

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True,
                             widget=forms.TextInput(attrs={"class": "form-control"}))
    nickname = forms.CharField(max_length=150, help_text='Your Nickname is what others see', required=True,
                               widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'nickname', 'password1', 'password2',)
        widgets = {'username': forms.TextInput(attrs={"class": "form-control"}), }


class AddPublicMatchSelectGameForm(forms.Form):
    add_public_game_title_id = forms.ModelChoiceField(queryset=GameTitle.objects.filter(public_allowed=True),
                                                      widget=forms.Select(attrs={'class': 'form-select'}),
                                                      label="Game title")


class AddPublicMatchForm(forms.ModelForm):
    dummy_game_title = forms.ModelChoiceField(queryset=None, label="Game title", blank=True, required=False)

    def __init__(self, current_user, game_title_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['p2_id'].widget.attrs["class"] = "form-select"
        self.fields['p1_score'].widget.attrs["class"] = "form-control"
        self.fields['p1_score'].widget.attrs["type"] = "number"
        self.fields['p1_score'].widget.attrs["min"] = "0"
        self.fields['p2_score'].widget.attrs["class"] = "form-control"
        self.fields['p2_score'].widget.attrs["type"] = "number"
        self.fields['p2_score'].widget.attrs["min"] = "0"
        self.fields['p1_character'].widget.attrs["class"] = "form-control"
        self.fields['p2_character'].widget.attrs["class"] = "form-control"
        self.fields['game_title_id'].widget.attrs["class"] = "form-select"
        self.fields['game_mode_id'].widget.attrs["class"] = "form-select"
        self.fields['game_mode_id'].queryset = self.fields['game_mode_id'].queryset.filter(
            gametitle=game_title_id).filter(public_allowed=True)
        self.fields['game_title_id'].queryset = self.fields['game_title_id'].queryset.filter(id=game_title_id)
        self.initial['game_title_id'] = self.fields['game_title_id'].queryset.filter(id=game_title_id).first()
        self.fields['game_title_id'].widget = forms.HiddenInput()
        self.fields['dummy_game_title'].queryset = self.fields['game_title_id'].queryset.filter(id=game_title_id)
        self.fields['dummy_game_title'].widget.attrs["class"] = "form-select"
        self.initial['dummy_game_title'] = self.fields['game_title_id'].queryset.filter(id=game_title_id).first()
        self.fields['dummy_game_title'].widget.attrs["disabled"] = True
        self.fields['p2_id'].queryset = self.fields['p2_id'].queryset.exclude(id=current_user.id)

        self.fields['p2_id'].label = 'Opponents nickname'
        self.fields['p1_score'].label = 'Your score'
        self.fields['p2_score'].label = 'Opponents score'
        self.fields['p1_character'].label = 'Your character'
        self.fields['p2_character'].label = 'Opponents character'
        self.fields['game_title_id'].label = 'Game Title'
        self.fields['game_mode_id'].label = 'Game Mode'

    class Meta:
        model = Score
        fields = ['p2_id', 'p1_score', 'p2_score', 'p1_character', 'p2_character', 'game_title_id',
                  'game_mode_id', 'score_confirmed', 'public_score']
        exclude = ['p1_id', 'score_confirmed', 'public_score']


class AddPersonalMatchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['p1_id'].widget.attrs["class"] = "form-select"
        self.fields['personal_opponent_nickname'].widget.attrs["class"] = "form-control"
        self.fields['p1_score'].widget.attrs["class"] = "form-control"
        self.fields['p1_score'].widget.attrs["type"] = "number"
        self.fields['p1_score'].widget.attrs["min"] = "0"
        self.fields['p2_score'].widget.attrs["class"] = "form-control"
        self.fields['p2_score'].widget.attrs["type"] = "number"
        self.fields['p2_score'].widget.attrs["min"] = "0"
        self.fields['p1_character'].widget.attrs["class"] = "form-control"
        self.fields['p2_character'].widget.attrs["class"] = "form-control"
        self.fields['game_title_id'].widget.attrs["class"] = "form-select"
        self.fields['game_mode_id'].widget.attrs["class"] = "form-select"
        # self.fields['score_confirmed'].widget.attrs["class"] = "form-check"
        # self.fields['public_score'].widget.attrs["class"] = "form-check"
        self.fields['game_title_id'].widget = forms.TextInput(attrs={"class": "form-control"})
        self.fields['game_mode_id'].widget = forms.TextInput(attrs={"class": "form-control"})

        self.fields['personal_opponent_nickname'].label = "Opponent nickname"
        self.fields['p1_score'].label = 'Your score'
        self.fields['p2_score'].label = 'Opponents score'
        self.fields['p1_character'].label = 'Your character'
        self.fields['p2_character'].label = 'Opponents character'
        self.fields['game_title_id'].label = 'Game Title'
        self.fields['game_mode_id'].label = 'Game Mode'

    class Meta:
        model = Score
        fields = ['personal_opponent_nickname', 'p1_score', 'p2_score', 'p1_character', 'p2_character', 'game_title_id',
                  'game_mode_id']
        exclude = ['p1_id', 'p2_id', 'score_confirmed', 'public_score']
