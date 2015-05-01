from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^patients/label/(?P<lbl_name>.+)/$', 'hit_server.views.getPatientsForLabel', name='getPatientsForLabel'),
    url(r'^patients/label/(?P<lbl_name>.+)/(?P<patient_id>.+)/$', 'hit_server.views.addLabelToPatient', name='addLabelToPatient'),
    url(r'^patients/(?P<patient_id>.+)/$', 'hit_server.views.getAllInfoForPatient', name='getAllInfoForPatient'),
    url(r'^filldbonce$', 'hit_server.views.refreshDBwithFHIR', name='fill_db'),
    url(r'^patients/$', 'hit_server.views.getPatient', name='getPatient'),
    url(r'^newlabel/$', 'hit_server.views.newlabel', name='newlabel'),
    url(r'^$', 'hit_server.views.login', name='login')
)
