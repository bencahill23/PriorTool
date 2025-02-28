import pandas as pd
import streamlit as st
import numpy as np
import random
import os
from tempfile import NamedTemporaryFile



#############
# IMPORT DATA
#############
@st.cache_data
def readExcel(pathToFile):
	importedData = pd.read_excel(pathToFile)
	keys = []
	for i in range(importedData.shape[0]):
		keys.append(str(random.randint(1,100000)))
	return [importedData,keys]

def categoryWidget(_category, _activity, _data, _keys):
	data =_data
	category = _category
	activity = _activity
	keys = _keys
	questions = []
	temp = []
	for i in range(data.shape[0]):
		at = data.iloc[i]['ACTIVITY_TYPE']
		cat = data.iloc[i]['CATEGORY']

		if (at == activity) and (cat == category):
			temp = [data.iloc[i]['QUESTION'],data.iloc[i]['QUESTION_TYPE'],data.iloc[i]['WEIGHT'], data.iloc[i]['CATEGORY'],keys[i]]
			questions.append(temp.copy())

	catResult = [None] *len(questions)# holder for data
	testCont = st.container(border=True)

	with testCont.container():
		headertext = category + " - " + activity
		st.header(headertext)
		for (i,q) in enumerate(questions):
			if q[1] == 'binary':
				cr = st.radio(q[0],['YES', 'NO'], horizontal=True)#, key = q[4])
				if cr == 'YES':
					cr = 1
				else:
					cr = 0

			elif q[1] == 'numeric':
				cr = st.number_input(q[0], step = 1)#, key = q[4]) # WHY DID I WRITE THIS key= ???

			catResult[i] = cr

		st.expander('Help for Value for ' + category).write("HELP TEXT TODO")
	return (questions.copy(), catResult.copy())




###################
# Header
###################
cola, colb = st.columns([4,1])
with cola:
	st.title('WBDK Prioritising Tool v.1.0')
with colb:
	st.image('assets/logo.jpg')


###################
# Import File Section
###################
impFileContainer = st.container(border = True) 
with impFileContainer.container():
	uploaded_file = st.file_uploader("Choose a file")
	if uploaded_file is not None:
		with NamedTemporaryFile(dir='.') as f:
			f.write(uploaded_file.getbuffer())
			data = readExcel(f.name)
	else:
		data = readExcel('assets/PriorTool_Input_Data.xlsx') # default Excel file




importedData = data[0]
keys = data[1]
numQuestions = importedData.shape[0]

# get the activity types list
allTypes = []
allCats = []
for i in range(numQuestions):
	allTypes.append(importedData.iloc[i]['ACTIVITY_TYPE'])
	allCats.append(importedData.iloc[i]['CATEGORY'])

actTypes = list(set(allTypes)) # list of uniques ACTIVITY TYPES
catTypes = list(set(allCats)) # list of uniques CATEGORIES




###################
# Activity Section
###################
actContainer = st.container(border = True) 
with actContainer.container():
	cola, colb = st.columns(2)
	with cola:
		actType = st.radio('Activity Type', actTypes)
	with colb:
		actTitle = st.text_input('Activity Title', 'Activity Title', label_visibility="collapsed")
		author = st.text_input('Activity Title', 'Author', label_visibility="collapsed")


#################
# ECONOMY SECTION 
#################
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
		economy_in = st.number_input('Economy gain for activity (DKK)', step = 1)
	with col2:
		economy_out = st.number_input('Economy loss for activity (DKK)', step = 1)

economy = economy_in - economy_out
ecoContainer.write('Total Economy: ' + str(economy) + ' DKK')

###################
#END ECONOMY SECTION
###################


###################
# Build GUI 
###################
responses = []
for cat in catTypes:
	#categoryWidget(cat, actType, importedData, keys)
	responses.append(categoryWidget(cat, actType, importedData, keys))


if st.button('SUBMIT REPONSE'):
	st.write("You saved your data")
	st.write(responses)

###################
# Summarise Responses
###################


categoryResponses = []
collectedResponses = []
weights =[]

print('-'*50)
for resp in responses:
	print('Questions -')
	print(resp[0])
	for questions in resp[0]:
		weights.append(questions[2])

	catWeights = weights.copy()
	weights = []


	collectedResponses.append([resp[1], catWeights])

	print('CAT RESPONSE')
	print(resp[1]) # answers set
	print(catWeights)
	print('*'*20) # answers


print('-'*50)
#print(responses[1][0][0])
#print(responses[0][0][0]) # question params for [category][questions = 1, reponses = 0][question number]
#print(responses[0][0][0][2]) # weight for a given question
#print(responses[0][1]) # reponses from section 0

#print(responses[1][1])

#
# Summary
#
# totalScores = [V4WBDKScore, V4MemberScore,V4SocScore]
# totalAverage = np.mean(totalScores)
# summaryContainer = st.container(border = True)

# with summaryContainer.container():
# 	st.header('Summary for ' + actTitle +' - ' + actType)
# 	st.write('Cost-per-lead: ' + str(costPerLead) + ' DKK')
# 	st.write('Value for WBDK: ' + str(V4WBDKScore))
# 	st.write('Value for Member: ' + str(V4MemberScore))
# 	st.write('Value for Society: ' + str(V4SocScore))
# 	st.write('-'*20)
# 	st.write('Total Score: ' + str(totalAverage))
# 	#V4SocScore

