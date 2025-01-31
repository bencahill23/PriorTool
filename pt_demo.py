import requests
import os
import json
import base64
 
import pandas as pd
import streamlit as st
import numpy as np

#Global Variables
actTypes = ['Conference','Network Meeting', 'Innovation Project']
actType = ''
economy = 0
V4WBDKScore = 0
numLeads = 0
V4WBDKSummary = []
V4MemberSummary = []
V4SocSummary = []



st.title('WBDK Prioritising Tool v.1.0')
actType = st.radio('Activity Type', actTypes)

# TITLE TEXT

actTitle = st.text_input('Activity Title', 'Descriptive Title')




#
# ECONOMY SECTION - Should be visible for all types
#
ecoHelpText = ''' 
Examples of (equivalent) positive income streams:  
Ticket Price  
Stand Rental   

A List of Stuff:  
1. THING  
2. THING  
3. OTHER THING  
  

REmember ABC  
'''
ecoContainer = st.container(border = True)
ecoContainer.header('Economy - ' + ' '+ actType)
with ecoContainer.container():
	st.expander('Help for Economy Calculations').write(ecoHelpText)

	ecoSubContainer = st.container(border = True)
	col1, col2, = st.columns(2)
	with col1:
		economy_in = st.number_input('Economy gain for activity (DKK)')
	with col2:
		economy_out = st.number_input('Economy loss for activity (DKK)')

economy = economy_in - economy_out
ecoContainer.write('Total Economy: ' + str(economy) + ' DKK')

#
#END ECONOMY SECTION
#




#
# Value for WBDK SECTION - Should be visible for all types
#
# NOTE multiline text field requires two spaces after each line.
V4WBDKHelpText = ''' Help to Evaluate Value for WBDK  
Another Line  
Another good tip  
Be Aware of XYX'''
V4WBDKContainer = st.container(border = True)
V4WBDKContainer.header('Value for WBDK -' + ' '+ actType)

with V4WBDKContainer.container():
	st.expander('Help for Value for WBDK Calculations').write(V4WBDKHelpText)


# Activity Type 1
if (actType == actTypes[0]):
	numLeads = V4WBDKContainer.number_input('Number of Leads Expected', min_value = 1, step = 1)
	speaker = V4WBDKContainer.radio('Speaker Role?',['YES', 'NO'], horizontal=True)
	stand = V4WBDKContainer.radio('WBDK Stand/Exhibit?',['YES', 'NO'], horizontal=True)
	cosender = V4WBDKContainer.radio('Member as co-sender?',['YES', 'NO'], horizontal=True)
	V4WBDKSummary = [numLeads, speaker, stand, cosender]


# Activity Type 2
if (actType == actTypes[1]):
	numLeads = V4WBDKContainer.number_input('Number of Leads Expected', min_value = 1, step = 1)
	focus = V4WBDKContainer.radio('Relevant Strategic Focus?',['YES', 'NO'], horizontal=True)
	projectFinancing = V4WBDKContainer.radio('Potential for Project Financing?',['YES', 'NO'], horizontal=True)
	V4WBDKSummary = [numLeads, focus, projectFinancing]


# Activity Type 3
if (actType == actTypes[2]):
	numLeads = 0
	knowledge = V4WBDKContainer.radio('Creation of new Knowledge?',['YES', 'NO'], horizontal=True)
	projectFinancing = V4WBDKContainer.radio('Potential for Additional Project Financing?',['YES', 'NO'], horizontal=True)
	mediaExposure = V4WBDKContainer.radio('Potential for Intnl Media Exposure?',['YES', 'NO'], horizontal=True)
	V4WBDKSummary = [numLeads, knowledge, projectFinancing, mediaExposure]

# TODO Calculate Weights, Averages and scores'
if V4WBDKSummary[0] > 0:
	costPerLead = economy/V4WBDKSummary[0]
else:
	costPerLead = 'N/A'

V4W = []
for (i,a) in enumerate(V4WBDKSummary):
	if (a == 'YES'):
		a = 1
	elif (a == 'NO'):
		a = 0
	V4W.append(a)

# V4W contains a list of the results from the Vlaue for WBDK Section
V4WBDKScore  = np.average(V4W[1:]) #(speakerScore + standScore + cosenderScore) /3
#Display scoring

#V4WBDKContainer.write('Total Score for Value for WBDK: ' + str(V4WBDKScore))

#
# END Value for WBDK Section
#



#
# Value for MEMBER SECTION - Should be visible for all types
#
# NOTE multiline text field requires two spaces after each line.
V4MemberHelpText = ''' Help to Evaluate Value for Membership Benefits  
Another Line  
Another good tip '''

V4MemberContainer = st.container(border = True)
V4MemberContainer.header('Value for Member -' + ' '+ actType)

with V4MemberContainer.container():
	st.expander('Help for Value for Member Calculations').write(V4MemberHelpText)


# Activity Type 1
if (actType == actTypes[0]):
	matchmaking = V4MemberContainer.radio('Matchmaking Activities?',['YES', 'NO'], horizontal=True)
	stagetime = V4MemberContainer.radio('Member Stand/Exhibit/Stagetime?',['YES', 'NO'], horizontal=True)
	V4MemberSummary = [matchmaking, stagetime]


# Activity Type 2
if (actType == actTypes[1]):
	relevance = V4MemberContainer.radio('Relevant Topics for Businesses?',['YES', 'NO'], horizontal=True)
	newKnowledge = V4MemberContainer.radio('New Knowledge?',['YES', 'NO'], horizontal=True)
	V4MemberSummary = [relevance, newKnowledge]


# Activity Type 3
if (actType == actTypes[2]):
	#numLeads = 0
	newKnowledge = V4MemberContainer.radio('New Knowledge?',['YES', 'NO'], horizontal=True)
	freeResources = V4MemberContainer.radio('Access to *Free* Resources?',['YES', 'NO'], horizontal=True)
	V4MemberSummary = [newKnowledge, freeResources]

# TODO Calculate Weights, Averages and scores'

V4M = []
for (i,a) in enumerate(V4MemberSummary):
	if (a == 'YES'):
		a = 1
	elif (a == 'NO'):
		a = 0
	V4M.append(a)

# V4W contains a list of the results from the Vlaue for WBDK Section
V4MemberScore  = np.average(V4M) #(speakerScore + standScore + cosenderScore) /3
#Display scoring

#V4WBDKContainer.write('Total Score for Value for WBDK: ' + str(V4WBDKScore))

#
# END Value for MEMBER Section
#



#
# Value for SOCIETY SECTION - Should be visible for all types
#
# NOTE multiline text field requires two spaces after each line.
V4SocHelpText = ''' Help to Evaluate Value for Societal Benefits  
Another Line  
Another good tip '''

V4SocContainer = st.container(border = True)
V4SocContainer.header('Value for Society -' + ' '+ actType)

with V4SocContainer.container():
	st.expander('Help for Value for Society Calculations').write(V4SocHelpText)


# Activity Type 1
if (actType == actTypes[0]):
	generalKnowledge = V4SocContainer.radio('Spread Knowledge to General Public?',['YES', 'NO'], horizontal=True)
	frontRunner = V4SocContainer.radio('WBDK positioned as frontrunner?',['YES', 'NO'], horizontal=True)
	V4SocSummary = [generalKnowledge, frontRunner]


# Activity Type 2
if (actType == actTypes[1]):
	xyz = V4SocContainer.radio('Relevant Political Link?',['YES', 'NO'], horizontal=True)
	xyz2 = V4SocContainer.radio('Potential to influence branch/industry?',['YES', 'NO'], horizontal=True)
	xyz3 = V4SocContainer.radio('Supports Sustainability?',['YES', 'NO'], horizontal=True)
	V4SocSummary = [xyz, xyz2, xyz3]


# Activity Type 3
if (actType == actTypes[2]):
	#numLeads = 0
	a1 = V4SocContainer.radio('Something?',['YES', 'NO'], horizontal=True)
	a2 = V4SocContainer.radio('Somehting Else?',['YES', 'NO'], horizontal=True)
	V4SocSummary = [a1, a2]

# TODO Calculate Weights, Averages and scores'

V4S = []
for (i,a) in enumerate(V4SocSummary):
	if (a == 'YES'):
		a = 1
	elif (a == 'NO'):
		a = 0
	V4S.append(a)

# V4W contains a list of the results from the Vlaue for WBDK Section
V4SocScore  = np.average(V4S) 

#
# END Value for SOCIETY Section
#


#
# Summary
#
totalScores = [V4WBDKScore, V4MemberScore,V4SocScore]
totalAverage = np.mean(totalScores)
summaryContainer = st.container(border = True)

with summaryContainer.container():
	st.header('Summary for ' + actTitle +' - ' + actType)
	st.write('Cost-per-lead: ' + str(costPerLead) + ' DKK')
	st.write('Value for WBDK: ' + str(V4WBDKScore))
	st.write('Value for Member: ' + str(V4MemberScore))
	st.write('Value for Society: ' + str(V4SocScore))
	st.write('-'*20)
	st.write('Total Score: ' + str(totalAverage))
	#V4SocScore

