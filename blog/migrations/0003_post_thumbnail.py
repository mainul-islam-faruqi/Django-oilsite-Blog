# Generated by Django 2.2.10 on 2020-07-06 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]