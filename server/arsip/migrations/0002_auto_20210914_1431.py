# Generated by Django 3.0.11 on 2021-09-14 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arsip', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suratmasuk',
            name='approve_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved', to='arsip.Pengguna'),
        ),
    ]
