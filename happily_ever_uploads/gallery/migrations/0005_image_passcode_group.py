# Generated by Django 5.1 on 2025-02-26 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_remove_image_caption_image_comment_image_name_and_more'),
        ('users', '0003_passcodegroup_customuser_passcode_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='passcode_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_images', to='users.passcodegroup'),
        ),
    ]
