# Generated by Django 2.1.7 on 2019-03-12 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageboard', '0003_board_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='description',
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
    ]