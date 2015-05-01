import requests
import json
import re

#serverURL = "https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/"
serverURL = "https://healthport.i3l.gatech.edu:8443/dstu1/fhir/"

# I left a bunch of snippets of code at the bottom of this to give some idea of how to handle these the dictionary being returned, + some other string slicing and regex methods.

def getPatientList():
    global serverURL
    list = []

    patientLiteral = r"Patient/"
    patientSanitizer = re.compile(patientLiteral, re.I)
  
    for i in range(10):
        payload = {'code': '174.' + str(i), '_format': 'json'}
        response = requests.get(serverURL + "Condition", params=payload, verify=False)
        patientList = json.loads(response.text)
        for entry in patientList['entry']:
            list.append(patientSanitizer.sub('', entry['content']["subject"]["reference"].encode('ascii')))
            
    return list
    
def getPatientContactInfo(patientID):
    global serverURL
    payload = {'_format': 'json'}
    response = requests.get(serverURL + "Patient/" + patientID, params=payload, verify=False)
    return response.json()
    
def getPatientObservations(patientID):
    global serverURL
    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get(serverURL + "Observation", params=payload, verify=False)
    return response.json()
    
def getPatientConditions(patientID):
    global serverURL
    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get(serverURL + "Condition", params=payload, verify=False)
    return response.json()

def getPatientMedications(patientID):
    global serverURL
    payload = {'subject:Patient': patientID, '_format': 'json'}
    response = requests.get(serverURL + "MedicationPrescription", params=payload, verify=False)
    return response.json()

def getAllPatientData(patientID):
    response = {}
    response['Contact Info'] = getPatientContactInfo(patientID)
    response['Observations'] = getPatientObservations(patientID)
    response['Conditions'] = getPatientConditions(patientID)
    response['Medications'] = getPatientMedications(patientID)
    return cleanJsonData(json.dumps(response))

def cleanJsonData(response):
    divRemove = re.compile(r'</?[a-zA-Z]{0,20}>')
    response = re.sub(divRemove, '', response)
    
    return dictGenerator(response)
    
def dictGenerator(response):
    jsonDict = {}
    jsonDict['Observations'] = observationsDict(response)
    jsonDict['Contact Info'] = patientDict(response)
    jsonDict['Conditions'] = conditionsDict(response)
    jsonDict['Medications'] = medicationsDict(response)
    
    return json.dumps(jsonDict)

def medicationsDict(response):
    response = json.loads(response)
    medicationsDict = {}
    for index, entry in enumerate(response['Medications']['entry']):
        temp = {}
        try:
            temp['name'] = entry['content']['medication']['display']
        except:
            pass
            
        try:
            temp['code'] = entry['content']['contained'][0]['code']['coding'][0]['code']
        except:
            pass
  
        try:
            temp['code_system'] = entry['content']['contained'][0]['code']['coding'][0]['system']
        except:
            pass
  
        try:
            temp['status'] = entry['content']['status']
        except:
            pass
        
        try:
            temp['perscriber'] = entry['content']['perscriber']['display']
        except:
            pass

        try:
            temp['dosage_text'] = entry['content']['dosageInstruction'][0]['text']
        except:
            pass

        try:
            temp['dosage_value'] = entry['content']['dosageInstruction'][0]['doseQuantity']['value']
        except:
            pass
            
        try:
            temp['dosage_units'] = entry['content']['dosageInstruction'][0]['doseQuantity']['units']
        except:
            pass
            
        try:
            temp['date_written'] = entry['content']['dateWritten']
        except:
            pass
            
        try:
            temp['patient'] = entry['content']["patient"]['reference']
        except:
            pass
            
        medicationsDict['Medication' + str(index + 1)] = temp
            
    return medicationsDict
    
def patientDict(response):
    response = json.loads(response)
    patientDict = {}
    try:
        patientDict['first_name'] = response['Contact Info']['name'][0]['given'][0]
    except:
        pass
        
    try:
        patientDict['last_name'] = response['Contact Info']['name'][0]['family'][0]
    except:
        pass
        
    return patientDict
  
def conditionsDict(response):
    response = json.loads(response)
    conditionsDict = {}
    for index, entry in enumerate(response['Conditions']['entry']):
        temp = {}
        try:
            temp['name'] = entry['content']['code']['coding'][0]['display']
        except:
            pass
            
        try:
            temp['code'] = entry['content']['code']['coding'][0]['code']
        except:
            pass
  
        try:
            temp['text'] = entry['content']['text']['div']
        except:
            pass
            
        try:
            temp['onset_date'] = entry['content']['onsetDate']
        except:
            pass
            
        try:
            temp['patient'] = entry['content']["subject"]['reference']
        except:
            pass
            
        conditionsDict['Condition' + str(index + 1)] = temp
            
    return conditionsDict
  
def observationsDict(response):
    response = json.loads(response)
    observationsDict = {}
    for index, entry in enumerate(response['Observations']['entry']):
        temp = {}
        try:
            temp['name'] = entry['content']['name']['coding'][0]['display']
        except:
            pass
            
        try:
            temp['code'] = entry['content']['name']['coding'][0]['code']
        except:
            pass

        try:
            temp['text'] = entry['content']["text"]['div']
        except:
            pass
            
        try:
            temp['value'] = entry['content']["valueQuantity"]['value']
        except:
            pass
            
        try:
            temp['units'] = entry['content']["valueQuantity"]['units']
        except:
            pass
        
        try:
            temp['date_time'] = entry['content']["appliesDateTime"]
        except:
            pass
        
        try:
            temp['patient'] = entry['content']["subject"]['reference']
        except:
            pass
        
        observationsDict['Observation' + str(index + 1)] = temp
    
    return observationsDict
    
def sqlInsert(patientDictionary):
    for entry in patientDictionary['Observations']:
        print entry
        for key, value in patientDictionary['Observations'][entry].viewitems():
            print str(key) + ': ' +str(value)
            #Insert sql code here. Note- I'm sure there are better ways to do this. Here is one example.

def StartApp():
    PatientData = {}
    
    Patients = getPatientList()
    for patient in Patients:
        PatientData[patient] = json.loads(getAllPatientData(patient))
    
    with open('hit_server/FHIRJsonResponse.json', 'wb') as f:
        f.write(json.dumps(PatientData))
        print "writing to json"
            
#if __name__ == "__main__":
    #Previously gathered breast cancer patient list
    #Patients = ['4.666034464-01', '4.000591657-01', '4.000792644-01', '4.899550000-01', '4.365006868-01', '4.666178052-01', '4.666621705-01', '4.952001152-01', '4.000985963-01', '4.667240000-01']
    
    #StartApp()
    
    # PatientData = {}
    # for patient in Patients:
        # PatientData[patient] = json.loads(getAllPatientData(patient))
    
    # with open('FHIRJsonResponse.json', 'wb') as f:
        # f.write(json.dumps(PatientData))
        
        # for key, value in response['Contact Info'].viewitems():
            # f.write('\t' + str(key) + ': ' +str(value) + '\n')
    
        # f.write('\n\nObservations:\n')
    
        # for entry in response['Observations']:
            # f.write('\t' + str(entry) + ':\n')
            # for key, value in response['Observations'][entry].viewitems():
                # f.write('\t\t' + str(key) + ': ' +str(value) + '\n')
        
        # f.write('\n\nConditions:\n')
    
        # for entry in response['Conditions']:
            # f.write('\t' + str(entry) + ':\n')
            # for key, value in response['Conditions'][entry].viewitems():
                # f.write('\t\t' + str(key) + ': ' +str(value) + '\n')
        
        # f.write('\n\nMedications:\n')
        
        # for entry in response['Medications']:
            # f.write('\t' + str(entry) + ':\n')
            # for key, value in response['Medications'][entry].viewitems():
                # f.write('\t\t' + str(key) + ': ' +str(value) + '\n')
        
    #this matches the entire section of the JSON that includes both instances of the link.
    # crawlJSON = re.compile(r'"link": \[\{[,":\/\.\-\w\d\s]+\}\], "id": [,":\/\.\-\w\d\s]+')
    # webLink = re.compile(r'https://taurus.i3l.gatech.edu:8443/HealthPort/fhir/Observation/[0-9.]+[-a-zA-Z]+')
    
    # for match in reversed(list(re.finditer(crawlJSON, response))):
        # print 'Match: ' + str(match.start())
        # #using re.findall to get a list of string matches, then grabbing the first
        # link = re.search(webLink, response[match.start():match.end()])
        # if link:
            # print 'Link Replace: ' + str(match.start())
            # payload = {'_format': 'json'}
            # jsonInsert = requests.get(link.group(), params=payload, verify=False)
            # #string slice to recombine json
            # response = response[:match.start()] + '"Additional Information": ' + jsonInsert.text + response[match.end():]
    
