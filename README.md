# CancerSurvivorshipCare
A web-based solution to create an SCP for physicians 

INSTRUCTIONS (to run)

1.	The app is hosted using heroku at https://hitscp.herokuapp.com/  . Please use the link to access it. 
2.	App Link: https://hitscp.herokuapp.com/
3.	Github link (source code): https://github.gatech.edu/asangal3/HITUI.git

Known issues: 
1.	Since heroku is a free service and our app loads a large chunk of FHIR data during the first login, please be advised that the first login might take longer than average. Up until now we have had the FHIR data pre-loaded but since the new url, we haven't been able to set up the database before login. 
2.	 Our database is periodically updated with the new FHIR data. We have tested this with the old url link, but not with the new url (https://healthport.i3l.gatech.edu:8443/dstu1/fhir/). If there is an issue, we can substitute the old url quite easily.


INSTRUCTIONS (to use)

1.	When you start the application, you can see a login page. We aren’t authenticating the login at this point of time so you can just press on the login to get to the main page.
2.	You can view a list of all patients that have breast cancer on the main page.
	a.	You can see the condition or diagnosis for the patient is on top.
	b.	The details about the most recent visit and time for that visit is visible.
	c.	The observation and treatment is shown on the main page on the right
3.	The main page also consists of the doctors’ notifications and messages.
	a.	These are hard-coded right now, but as our application progresses it can be dynamic.
4.	When you press “More details”, it takes you to the profile of each patient that has all the information about the patient.
	a.	It consists of the basic profile of the patient. This profile also provides a timeline for the patients visit to this particular doctor.
	b.	The SCP chart that the PCP, nurse, oncologist can fill and keep notes on a patient
	c.	The tests that were performed on the patients and the observations in color-coded format.
5.	Labels: This is our value addition over the usual doctor interface, where a doctor can add his/her customized labels to a patient and then sort patients by these labels. 
	a.	In the patient detail page, click on “add label”. Once a label is added it will show up on your side bar. 
	b.	If you add two or more patients with the same label you can filter out those patients from the home page by clicking that label.

