from Game_Ranking_System.models import Score


def extras(request):
    """Method adding a custom context processor returning True if user has pending scores to confirm.
    Used in base template so the notification is visible on each subpage"""

    pending_scores_to_confirm = True if len(
        Score.objects.filter(score_confirmed=False).filter(p2_id=request.user.id)) > 0 else False
    return {'pending_scores_to_confirm': pending_scores_to_confirm}
