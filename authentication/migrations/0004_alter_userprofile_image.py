# Generated by Django 5.1.1 on 2024-11-24 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_roles_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='profile_pictures/default.png', upload_to='profile_pictures/'),
        ),
    ]
