# Generated by Django 4.0.2 on 2022-10-21 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Game_Ranking_System', '0004_auto_20220930_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicscore',
            name='creator_id',
        ),
        migrations.RemoveField(
            model_name='publicscore',
            name='game_mode_id',
        ),
        migrations.RemoveField(
            model_name='publicscore',
            name='game_title_id',
        ),
        migrations.RemoveField(
            model_name='publicscore',
            name='opponent_id',
        ),
        migrations.RemoveField(
            model_name='publicscore',
            name='score',
        ),
        migrations.AddField(
            model_name='score',
            name='game_mode_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Game_Ranking_System.gamemode'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='game_title_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Game_Ranking_System.gametitle'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='score',
            name='public_score',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='score',
            name='score_confirmed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='score',
            name='p1_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='score',
            name='p2_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opponent_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='PrivateScore',
        ),
        migrations.DeleteModel(
            name='PublicScore',
        ),
    ]
