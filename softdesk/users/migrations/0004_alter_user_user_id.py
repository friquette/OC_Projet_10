# Generated by Django 3.2.6 on 2021-09-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]