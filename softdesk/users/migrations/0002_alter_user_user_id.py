# Generated by Django 3.2.6 on 2021-09-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
