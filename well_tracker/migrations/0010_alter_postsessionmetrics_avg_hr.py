# Generated by Django 5.1.4 on 2024-12-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('well_tracker', '0009_alter_presessionmetrics_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsessionmetrics',
            name='avg_HR',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
