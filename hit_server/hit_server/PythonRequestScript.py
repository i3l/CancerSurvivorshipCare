import requests
import json
import re

def getPatientList():
    list = []

    patientRegex = r"Patient/[0-9.-]+"
    patientParse = re.compile(patientRegex)
    patientLiteral = r"Patient/"
    patientSanitizer = re.compile(patientLiteral, re.I)

    payload = {'code': '174.9', '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Condition", params=payload, verify=False)
    patientList = response.text
    tempList = re.findall(patientParse, patientList)
    for patient in tempList:
        getPatient(patientSanitizer.sub('', patient))

    return list

def getPatient(patientID, bool):
    if bool:
        text_file.write(",")

    dictall = {}

    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Observation", params=payload, verify=False)
    dictall['Observation'] = response
    text_file.write(response.text)
    text_file.write(",")
    #observations = response.text

    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Condition", params=payload, verify=False)
    text_file.write(response.text)
    
    text_file.write(",")
    #conditions = response.text

    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/MedicationPrescription", params=payload, verify=False)
    text_file.write(response.text)

    return


def getPatientContactInfo(patientID):
    payload = {'_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Patient/" + patientID, params=payload, verify=False)
    return response.json()
    
def getPatientObservations(patientID):
    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Observation", params=payload, verify=False)
    return response.json()
    
def getPatientConditions(patientID):
    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Condition", params=payload, verify=False)
    return response.json()

def getPatientMedications(patientID):
    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get("https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/MedicationPrescription", params=payload, verify=False)
    return response.json()    

def getAllPatientData(patientID):
    response = '{'
    response = response + "\"Contact Info\": " + getPatientContactInfo(patientID)
    response = response + "\"Observations\": " + getPatientObservations(patientID)
    response = response + "\"Conditions\": " + getPatientConditions(patientID)
    response = response + "\"Medications\": " + getPatientMedications(patientID)
    response = response + '}'
    return response

if __name__ == "__main__":
    Patients = ['4.666034464-01', '4.000591657-01', '4.000792644-01', '4.899550000-01', '4.365006868-01', '4.666178052-01', '4.666621705-01', '4.952001152-01', '4.000985963-01', '4.667240000-01']
    global text_file
    global bool
    text_file = open("CancerJSON.txt", "w")

    text_file.write("[")
    bool = False
    for patient in Patients:
        global bool
        getPatient(patient, bool)
        bool = True

    text_file.write("]")
