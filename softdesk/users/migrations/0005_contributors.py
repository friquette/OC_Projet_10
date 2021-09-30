# Generated by Django 3.2.6 on 2021-09-03 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_id', models.IntegerField()),
                ('permission', models.CharField(max_length=30)),
                ('role', models.CharField(max_length=30)),
            ],
        ),
    ]