# Generated by Django 2.2.1 on 2020-03-10 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiv1', '0013_auto_20200310_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='apiv1.Form'),
        ),
    ]