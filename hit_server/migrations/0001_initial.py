# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('condition_name', models.CharField(max_length=500)),
                ('onset_date', models.DateTimeField()),
                ('condition_code', models.CharField(max_length=500)),
                ('condition_desc', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('med_status', models.CharField(max_length=500)),
                ('med_name', models.CharField(max_length=500)),
                ('med_code', models.CharField(max_length=500)),
                ('med_dosage_value', models.FloatField()),
                ('med_dosage_text', models.CharField(max_length=500)),
                ('med_dosage_units', models.CharField(max_length=500)),
                ('med_date_written', models.DateTimeField(max_length=500)),
                ('med_code_system', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obs_code', models.CharField(max_length=500)),
                ('obs_name', models.CharField(max_length=500)),
                ('obs_desc', models.CharField(max_length=500)),
                ('obs_value', models.FloatField()),
                ('obs_units', models.CharField(max_length=500)),
                ('obs_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='PatientInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pid', models.CharField(max_length=500)),
                ('first_name', models.CharField(max_length=500)),
                ('last_name', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='observation',
            name='obs_for_patients',
            field=models.ForeignKey(related_name='obs_for_patients', to='hit_server.PatientInfo', null=True),
        ),
        migrations.AddField(
            model_name='medication',
            name='medication_for_patients',
            field=models.ForeignKey(related_name='medications_for_patient', to='hit_server.PatientInfo', null=True),
        ),
        migrations.AddField(
            model_name='label',
            name='patients_with_label',
            field=models.ManyToManyField(related_name='labels_for_patient', to='hit_server.PatientInfo'),
        ),
        migrations.AddField(
            model_name='condition',
            name='condition_for_patients',
            field=models.ForeignKey(related_name='conditions_for_patient', to='hit_server.PatientInfo', null=True),
        ),
    ]
