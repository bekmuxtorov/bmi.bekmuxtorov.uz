# Generated by Django 4.2 on 2024-05-23 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_daily_use'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='daily_use',
            field=models.IntegerField(blank=True, default=3, null=True, verbose_name='Kunlik foydalanish imkoniyati'),
        ),
    ]
