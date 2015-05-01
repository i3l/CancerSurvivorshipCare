import json
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from models import PatientInfo, Condition, Medication, Observation, Label
from django.shortcuts import render_to_response
#Right not there is only a login view, once more views are added this file can be updates/generated likewise.
from PythonRequestScript import *	
import os.path
import pickle
import datetime

def login(request):
	print "In logn"
	template = loader.get_template('login.html')
	context = RequestContext(request, {})

	shouldstartapp = False

	try:
		fileinput = open('timestamp.pkl', 'rb')
		tpdict = pickle.load(fileinput)
		fileinput.close()

		print ("last_login" in tpdict.keys()) , (abs(tpdict["last_login"] - datetime.datetime.now()).days )
		if "last_login" in tpdict.keys() and abs(tpdict["last_login"] - datetime.datetime.now()).days > 1: 
			shouldstartapp = True
			
	except:
		shouldstartapp = True	
		pass

	if shouldstartapp:
		print "Start App"
		StartApp()

		output = open('timestamp.pkl', 'wb')
		pickle.dump({"last_login":datetime.datetime.now()}, output)
		output.close()
    
		if not os.path.isfile("random.txt"):
			refreshDBwithFHIR(request)	
			dbfile = open("random.txt", 'w')
			dbfile.close()

	print "Check the json"
	return HttpResponse(template.render(context))

def newlabel(request):
    return render_to_response('newlabel.html', context_instance=RequestContext(request))

def listOfLabels():
    labels = Label.objects.all()
    alllbl = []
    for l in labels:
        alllbl.append(l.label_name)
    return alllbl

def minimalPatientResponseDict(p):
    responsedict = {}
    responsedict["pid"]=p.pid
    responsedict["first_name"]=p.first_name
    responsedict["last_name"]=p.last_name
    #Patient labels
    responsedict["labels"] = [lbl.label_name for lbl in p.labels_for_patient.all()]
    #conditions needed for patient
    if len(p.conditions_for_patient.all()) > 0:
        responsedict["condition_name"] = p.conditions_for_patient.all()[0].condition_name
        responsedict["condition_code"] = p.conditions_for_patient.all()[0].condition_code
        responsedict["condition_desc"] = p.conditions_for_patient.all()[0].condition_desc
    #observations needed for patient
    all_obs = p.obs_for_patients.all().order_by('-obs_date')

    if len(all_obs) > 0:
        responsedict["latest_observation"] = all_obs[0].obs_desc
        datetime =  str(all_obs[0].obs_date)

        datetime = datetime.split(' ')
        responsedict["latest_observation_date"] = datetime[0]
        responsedict["latest_observation_time"] = datetime[1]
        responsedict["latest_observation_name"] = all_obs[0].obs_name
        
    all_meds = p.medications_for_patient.filter(med_status='active')
    all_info_of_med = []
    for meds in all_meds:
        tempdict = {}
        tempdict["medication_name"] = meds.med_name
        tempdict["medication_code"] = meds.med_code
        tempdict["medication_value"] = meds.med_dosage_value
        tempdict["medication_units"] = meds.med_dosage_units
        tempdict["medication_text"] = meds.med_dosage_text
        tempdict["medication_date"] = meds.med_date_written
        all_info_of_med.append(tempdict)
    responsedict["active_medication"] = all_info_of_med
    return responsedict

def getPatient(request):
	# allpatients = []
    return getPatientsForLabel(request,'latest')
	# patients = PatientInfo.objects.all()
	# for p in patients:
	# 	allpatients.append(minimalPatientResponseDict(p))


def getResponseForPatient(patient_info):
	responsedict = {}
	responsedict["pid"] = patient_info[0].pid
	responsedict["first_name"] = patient_info[0].first_name
	responsedict["last_name"] = patient_info[0].last_name
	responsedict["labels"] = [lbl.label_name for lbl in patient_info[0].labels_for_patient.all()]
	#conditions needed for patient\
	all_condition_for_patient = []
	for condition in patient_info[0].conditions_for_patient.all():
		tempdict = {}
		tempdict["condition_name"] = condition.condition_name
		tempdict["condition_code"] = condition.condition_code
		tempdict["condition_desc"] = condition.condition_desc
		tempdict["onset_date"] = str(condition.onset_date)
		all_condition_for_patient.append(tempdict)

	responsedict["Conditions"] = all_condition_for_patient

	#all observations for patient
	all_observation_for_patient = []
	for observation in patient_info[0].obs_for_patients.all():
		tempdict = {}
		tempdict["obs_name"] = observation.obs_name
		tempdict["obs_code"] = observation.obs_code
		tempdict["obs_desc"] = observation.obs_desc
		tempdict["obs_date"] = str(observation.obs_date)
		tempdict["value"] = observation.obs_value
		tempdict["units"] = observation.obs_units
		all_observation_for_patient.append(tempdict)

	responsedict["Observations"] = all_observation_for_patient

	#all medications for 1 patient
	all_medication_for_patient = []
	for medication in patient_info[0].medications_for_patient.all():
		tempdict = {}
		tempdict["med_name"] = medication.med_name
		tempdict["med_code"] = medication.med_code
		tempdict["med_status"] = medication.med_status
		tempdict["dosage_value"] = medication.dosage_value
		tempdict["dosage_text"] = medication.dosage_text
		tempdict["dosage_units"] = medication.dosage_units
		tempdict["date_written"] = medication.date_written
		tempdict["code_system"] = medication.code_system
		all_medication_for_patient.append(tempdict)

	responsedict["Medications"] = 	all_medication_for_patient

	return responsedict

def getAllInfoForPatient(request,patient_id):
	print "***"
	patient_info = PatientInfo.objects.filter(pid=patient_id)
	responsedict = {}
	print "found ", len(patient_info), "Patients for pid ", patient_id, "from ", len(PatientInfo.objects.all())
	if len(patient_info) < 1:
		pass
	else:
		responsedict=getResponseForPatient(patient_info)

	# return render_to_response('index_2.html', {"patients":responsedict} , context_instance=RequestContext(request))
	# return HttpResponse (json.dumps(responsedict))
	return render_to_response('profile.html', {"p":responsedict,"labels":listOfLabels()} , context_instance=RequestContext(request))


#Helper: Add label "all" whenever refreshDBwithFHIR
# def addAllLabel():
#     all_patients = PatientInfo.objects.exclude(labels_for_patient__label_name="all")
#     print all_patients

def refreshDBwithFHIR(request):
	#get json from dir
	with open("hit_server/FHIRJsonResponse.json") as data_file:
		data = json.load(data_file)

	for p in data.keys():
		print p, data[p]["Contact Info"]["first_name"], data[p]["Contact Info"]["last_name"]
		patientobj = PatientInfo()  			# create a patient object.
		patientobj.pid = p
		patientobj.first_name = data[p]["Contact Info"]["first_name"]
		patientobj.last_name = data[p]["Contact Info"]["last_name"]
		patientobj.save()

		#first add all conditions to patient?

		all_conditions = data[p]["Conditions"].keys()
		for con in all_conditions:
			conditionobj = Condition()
			conditionobj.condition_name = data[p]["Conditions"][con]["name"]
			conditionobj.onset_date = data[p]["Conditions"][con]["onset_date"]
			conditionobj.condition_code = data[p]["Conditions"][con]["code"]
			conditionobj.condition_desc = data[p]["Conditions"][con]["text"]
			conditionobj.condition_for_patients = patientobj   # how to use related object

			conditionobj.save()

		all_medications = data[p]["Medications"].keys()

		if len(all_medications) == 0:
			pass

		else:
			for meds in all_medications:
				medicationobj = Medication()
				medicationobj.med_status = data[p]["Medications"][meds]["status"]
				medicationobj.med_name = data[p]["Medications"][meds]["name"]
				medicationobj.med_code = data[p]["Medications"][meds]["code"]
				medicationobj.med_dosage_value = data[p]["Medications"][meds]["dosage_value"]
				medicationobj.med_dosage_text = data[p]["Medications"][meds]["dosage_text"]
				medicationobj.med_dosage_units = data[p]["Medications"][meds]["dosage_units"]
				medicationobj.med_date_written = data[p]["Medications"][meds]["date_written"]
				medicationobj.med_code_system = data[p]["Medications"][meds]["code_system"]


				medicationobj.medications_for_patients = patientobj   # how to use related object

				medicationobj.save()


		all_observations = data[p]["Observations"].keys()
		for obs in all_observations:
			observationobj = Observation()
			observationobj.obs_name = data[p]["Observations"][obs]["name"]
			observationobj.obs_code = data[p]["Observations"][obs]["code"]
			observationobj.obs_desc = data[p]["Observations"][obs]["text"]

			check_existance_of_value = data[p]["Observations"][obs].keys()
			if "value" in check_existance_of_value:
				observationobj.obs_value = data[p]["Observations"][obs]["value"]
			else:
				observationobj.obs_value = 0.0

			if "units" in check_existance_of_value:
				observationobj.obs_units = data[p]["Observations"][obs]["units"]
			else:
				observationobj.obs_units = "NULL"


			observationobj.obs_date = data[p]["Observations"][obs]["date_time"]

			observationobj.obs_for_patients = patientobj   # how to use related object

			observationobj.save()

	return HttpResponse()

	'''
	# it gets added a lot of times because everytime the url is refreshed. This needs to occur only once in the beginning?
	# TODO
	'''

def addLabelToPatient(request,lbl_name,patient_id):
    patients_with_id = PatientInfo.objects.filter(pid = patient_id)
    labels_with_name = Label.objects.filter(label_name = lbl_name)
    patient = None
    label = None

    print "Adding label to Patient"

    if len(patients_with_id)>0:
        patient = patients_with_id[0]
    if len(labels_with_name)>0:
        label = labels_with_name[0]
    else:
        label = Label()
        label.label_name = lbl_name
        label.save()

    label.patients_with_label.add(patient)
    return HttpResponse()

def getPatientsForLabel(request,lbl_name):
    patients = []
    retDict = []
    print "Getting Patients for Label"
    if lbl_name == "all":
        patients = PatientInfo.objects.all()
    else:
        labels_with_name = Label.objects.filter(label_name = lbl_name)
        if len(labels_with_name) >0:
            patients = labels_with_name[0].patients_with_label.all()


    for p in patients:
        retDict.append(minimalPatientResponseDict(p))
    # return HttpResponse(json.dumps(retDict))
    return render_to_response('index.html', {"patients":retDict, "labels":listOfLabels()} , context_instance=RequestContext(request))
