# Generated by Django 3.2.6 on 2021-09-24 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210924_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='project_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='projects.projects'),
        ),
    ]
