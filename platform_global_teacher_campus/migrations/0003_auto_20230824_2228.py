# Generated by Django 3.2.19 on 2023-08-24 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platform_global_teacher_campus', '0002_auto_20230824_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='validationprocessevent',
            name='status',
            field=models.CharField(choices=[('subm', 'Submitted'), ('revi', 'In Review'), ('drft', 'Draft'), ('aprv', 'Approved'), ('dprv', 'Disapproved'), ('cncl', 'Cancelled'), ('exmp', 'Exempt')], default='subm', max_length=5),
        ),
        migrations.AlterField(
            model_name='validationprocessevent',
            name='validation_process',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='platform_global_teacher_campus.validationprocess'),
        ),
    ]
