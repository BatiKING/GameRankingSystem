# Generated by Django 4.0.2 on 2022-09-30 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game_Ranking_System', '0003_gamemode_gametitle_privatescore_publicscore_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatescore',
            name='id',
        ),
        migrations.RemoveField(
            model_name='privatescore',
            name='score_id',
        ),
        migrations.RemoveField(
            model_name='publicscore',
            name='id',
        ),
        migrations.RemoveField(
            model_name='publicscore',
            name='score_id',
        ),
        migrations.AddField(
            model_name='privatescore',
            name='score',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Game_Ranking_System.score'),
        ),
        migrations.AddField(
            model_name='publicscore',
            name='score',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Game_Ranking_System.score'),
        ),
    ]
