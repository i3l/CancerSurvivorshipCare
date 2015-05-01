from django.db import models

#table for patient info
class PatientInfo(models.Model):
	pid = models.CharField(max_length=500)
	first_name = models.CharField(max_length=500)
	last_name = models.CharField(max_length=500)
	#oid = models.ForeignKey('Observation', related_name="oid")

# this is for admin level debugging. It returns this string when this class is printed
	def __unicode__(self):
		return self.first_name

#table for observations
class Observation(models.Model):
	obs_code = models.CharField(max_length=500)
	obs_name = models.CharField(max_length=500)
	obs_desc = models.CharField(max_length=500)
	obs_value = models.FloatField()
	obs_units  = models.CharField(max_length=500)
	obs_date = models.DateTimeField()
	obs_for_patients = models.ForeignKey(PatientInfo, null=True, related_name = 'obs_for_patients')


	def __unicode__(self):
		return self.obs_name

#table for conditions
class Condition(models.Model):
	condition_name = models.CharField(max_length=500)
	onset_date = models.DateTimeField()
	condition_code = models.CharField(max_length=500)
	condition_desc = models.CharField(max_length=500)
	condition_for_patients = models.ForeignKey(PatientInfo, null=True, related_name ='conditions_for_patient')

	def __unicode__(self):
		return self.condition_name


#table for medication
class Medication(models.Model):
	med_status = models.CharField(max_length=500)
	med_name = models.CharField(max_length=500)
	med_code = models.CharField(max_length=500)
	med_dosage_value = models.FloatField()
	med_dosage_text = models.CharField(max_length=500)
	med_dosage_units = models.CharField(max_length=500)
	med_date_written = models.DateTimeField(max_length=500)
	med_code_system = models.CharField(max_length=500)
	medication_for_patients = models.ForeignKey(PatientInfo, null=True,  related_name ='medications_for_patient')

	def __unicode__(self):
		return self.med_name


class Label(models.Model):
	label_name = models.CharField(max_length=100)
	patients_with_label = models.ManyToManyField(PatientInfo, related_name="labels_for_patient")
