# Generated by Django 4.2.2 on 2023-11-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_platform', '0002_music_uploads_model_protected_accessors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artists',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name=300)),
                ('url', models.URLField(null=True)),
                ('picture_url', models.URLField(null=True)),
            ],
        ),
    ]
