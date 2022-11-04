from Game_Ranking_System.views import RankingView
from Game_Ranking_System.models import Score, User
from django.urls import reverse
import pytest


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_if_personal_score_added(client, dummy_users):
    client.force_login(user=User.objects.first())
    client.post(reverse('add_personal'), {'personal_opponent_nickname': 'TestOpponent1', 'p1_score': 10, 'p2_score': 4,
                                          'p1_character': 'TestChar1', 'p2_character': 'TestChar2',
                                          'game_title_id': 'TestGameTitle1', 'game_mode_id': 'TestGameMode1'})
    assert len(Score.objects.all()) == 1
    assert Score.objects.first().personal_opponent_nickname == 'TestOpponent1'
    assert Score.objects.first().game_mode_id.mode == "TestGameMode1"
    assert Score.objects.first().game_title_id.title == "TestGameTitle1"


def test_if_unknown_user_gets_redirected(client):
    response = client.get(reverse('personal'))
    assert response.status_code == 302
    response = client.get(reverse('add_public'))
    assert response.status_code == 302
    response = client.get(reverse('add_personal'))
    assert response.status_code == 302
    response = client.get(reverse('ranking'))
    assert response.status_code == 302
    response = client.get(reverse('confirm_score'))
    assert response.status_code == 302
    response = client.get(reverse('delete_score_request', kwargs={"match_id": 1}))
    assert response.status_code == 302
    response = client.get(reverse('confirm_score_request', kwargs={"match_id": 1}))
    assert response.status_code == 302


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_ranking_view(client, dummy_game_modes, dummy_game_titles, dummy_users, score_queryset):
    # client.login(username='TestUser1', password='TestPass1')
    client.force_login(user=User.objects.first())
    response = client.get(reverse('ranking'))
    assert response.status_code == 200
    assert len(response.context['ranking_data']) == 2


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_score_model(dummy_game_modes, dummy_game_titles, dummy_users, score_queryset):
    for obj in score_queryset:
        assert obj == Score.objects.get(pk=obj.pk)


class Object(object):
    pass


TEST_DATA = (
    ("Test1", "Test2", True),
    ("Test1", "Test2", True),
    ("Test1", "Test2", True),
    ("Test3", "Test2", True),
    ("Test3", "Test2", True),
    ("Test3", "Test2", False),

)
TEST_OUTPUT = {
    "Test1": {"matches_played": 3, "wins": 3},
    "Test2": {"matches_played": 6, "wins": 1},
    "Test3": {"matches_played": 3, "wins": 2},
}

TEST_INPUTS = []
for td in TEST_DATA:
    test_input = Object()
    test_input.p1_id = Object()
    test_input.p1_id.nickname = td[0]
    test_input.p2_id = Object()
    test_input.p2_id.nickname = td[1]
    test_input.p1_win = td[2]
    TEST_INPUTS.append(test_input)

TEST_DATA_FOR_ASSERTION = (
    [TEST_INPUTS, TEST_OUTPUT],
)


@pytest.mark.parametrize("ranking_input, ranking_output", TEST_DATA_FOR_ASSERTION)
def test_get_ranking_data(ranking_input, ranking_output):
    rv = RankingView.get_ranking_data(ranking_input)
    assert rv == ranking_output
