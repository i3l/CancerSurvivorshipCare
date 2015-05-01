import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime, timedelta

# Other Imports
from ..models import PatientInfo, Observation, Condition, Medication

@csrf_exempt
def getObservation(request, user_id):
	response_data = {}
	if user_id:
		observations = Observation.objects.filter(pid=user_id)
		
		#Ideally there shouldn't be duplicate users.

		response_data = observations.getResponseData()

		else:
			errorMessage = "Error! This user doesn't exist."
			return HttpResponse(json.dumps({'success': False, "error":errorMessage}), content_type="application/json")			

	return HttpResponse(json.dumps(response_data), content_type="application/json")

