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
	st.title('WBDK Prioritising Tool v.1.1')
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

Examples of (equivalent) negative income streams:  
Travel costs  
Hours  
'''
cost_per_lead = 0
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

	if actType == 'Conference':
		num_leads = st.number_input('Leads Expected', step = 1)
		if (num_leads):
			cost_per_lead = int(economy/num_leads)


ecoContainer.write('Total Economy: ' + str(economy) + ' DKK')
ecoContainer.write('Cost Per Lead: ' + str(cost_per_lead) + ' DKK' )

###################
#END ECONOMY SECTION
###################

###################
# Build GUI 
###################
responses = []
for cat in catTypes:
	responses.append(categoryWidget(cat, actType, importedData, keys))

###################
# Summarise Responses
###################


categoryResponses = []
collectedResponses = []
collectedWeights = []
collectedQuestions = []
weightedResult = []
weights =[]


for resp in responses:
	for questions in resp[0]:
		collectedQuestions.append(questions[0])
		weights.append(questions[2])

	catWeights = weights.copy()
	weights = []
	collectedResponses.append(resp[1])#, catWeights])
	collectedWeights.append(catWeights.copy())

for i,response in enumerate(collectedResponses):
	for j in range(len(response)):
		weightedResult.append(collectedResponses[i][j] * collectedWeights[i][j])

flat_weighs_list = [
    x
    for xs in collectedWeights
    for x in xs
]

overall_result = np.mean(weightedResult) / np.mean(flat_weighs_list)

###################
# Generate Responses
###################

category_reponses = []
for r in responses:
	resps =  r[1]
	cat_title = r[0][0][3]
	tmp_wght = []
	for cat in r[0]:
		tmp_wght.append(cat[2])

	categoryResponses.append([cat_title, resps, tmp_wght.copy()])


if st.button('SUBMIT REPONSE'):
	st.header('Overall Scores')
	st.write('Total Economy: ' + str(economy) + ' DKK')
	if cost_per_lead:
		st.write('Cost Per Lead: ' + str(cost_per_lead) + ' DKK')
	st.write('Overall Score: ' + str(int(overall_result*100)) + '%')
	st.header('Category Scores')
	for cat in categoryResponses:
		scr = (cat[1])
		wt = (cat[2])
		weighted = np.multiply(scr, wt)


		st.write(str(cat[0]) + ' Score: ' + str(int((np.mean(weighted)/np.mean(wt))*100)) + '%')
