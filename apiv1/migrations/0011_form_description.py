# Generated by Django 2.2.1 on 2020-03-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiv1', '0010_auto_20200309_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='description',
            field=models.CharField(default=' ', max_length=2048),
            preserve_default=False,
        ),
    ]