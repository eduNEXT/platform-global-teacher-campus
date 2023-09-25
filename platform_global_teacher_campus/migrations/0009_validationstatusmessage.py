# Generated by Django 3.2.19 on 2023-09-21 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_global_teacher_campus', '0008_alter_validationbody_validators'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationStatusMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('subm', 'Submitted'), ('revi', 'In Review'), ('drft', 'Draft'), ('aprv', 'Approved'), ('dprv', 'Disapproved'), ('cncl', 'Cancelled'), ('exmp', 'Exempt')], max_length=5, unique=True)),
                ('message', models.TextField(default='')),
                ('button', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
