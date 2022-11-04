import pytest
from django.test import Client
from Game_Ranking_System.models import Score, GameMode, GameTitle, User


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def dummy_users():
    User.objects.create(username="TestUser1", password="TestPass1", nickname="TestUser1")
    User.objects.create(username="TestUser2", password="TestPass2", nickname="TestUser2")
    User.objects.create(username="TestUser3", password="TestPass3", nickname="TestUser3")

@pytest.fixture
def dummy_game_modes():
    GameMode.objects.create(mode="TestMode1")
    GameMode.objects.create(mode="TestMode2")

@pytest.fixture
def dummy_game_titles():
    GameTitle.objects.create(title="TestTitle1")
    GameTitle.objects.create(title="TestTitle2")

@pytest.fixture
def set_modes_for_titles():
    for title in GameTitle.objects.all():
        title.mode.set(GameMode.objects.all())

@pytest.fixture(scope='function')
def score_queryset():
    s1 = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=10, p2_score=9, p1_character="TestChar1",
                              p2_character="TestChar2", game_title_id_id=1, game_mode_id_id=1, score_confirmed=True,
                              public_score=True)
    s2 = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=11, p2_score=9, p1_character="TestChar1",
                              p2_character="TestChar2", game_title_id_id=1, game_mode_id_id=1, score_confirmed=True,
                              public_score=True)
    s3 = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=12, p2_score=9, p1_character="TestChar1",
                              p2_character="TestChar2", game_title_id_id=1, game_mode_id_id=1, score_confirmed=True,
                              public_score=True)
    s4 = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=8, p2_score=9, p1_character="TestChar1",
                              p2_character="TestChar2", game_title_id_id=1, game_mode_id_id=1, score_confirmed=True,
                              public_score=True)
    s5 = Score.objects.create(p1_id_id=1, p2_id_id=2, p1_score=8, p2_score=9, p1_character="TestChar1",
                              p2_character="TestChar2", game_title_id_id=1, game_mode_id_id=1, score_confirmed=True,
                              public_score=False)
    s6 = Score.objects.create(p1_id_id=1, p2_id_id=3, p1_score=8, p2_score=9, p1_character="TestChar1",
                              p2_character="TestChar3", game_title_id_id=1, game_mode_id_id=1, score_confirmed=False,
                              public_score=True)
    list_of_ids = [s1.id, s2.id, s3.id, s4.id, s5.id, s6.id]
    return Score.objects.filter(pk__in=list_of_ids)
    # yield Score.objects.filter(pk__in=list_of_ids)
    # Score.objects.all().delete()

