# Generated by Django 2.2 on 2020-10-21 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201021_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_owners',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owns_jobs', to='main.User'),
        ),
    ]
