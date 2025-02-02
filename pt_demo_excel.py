import pandas as pd
import streamlit as st
import numpy as np
import random




#############
# IMPORT DATA
#############
@st.cache_data
def readExcel():
	importedData = pd.read_excel('assets/PriorTool_Input_Data.xlsx')
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
		#print(cat)
		if (at == activity) and (cat == category):
			temp = [data.iloc[i]['QUESTION'],data.iloc[i]['QUESTION_TYPE'],data.iloc[i]['WEIGHT'], data.iloc[i]['CATEGORY'],keys[i]]
			questions.append(temp)

	catResult = [None] *len(questions)# holder for data
	testCont = st.container(border=True)

	with testCont.container():
		headertext = category + " - " + activity
		st.header(headertext)
		for (i,q) in enumerate(questions):
			if q[1] == 'binary':
				catResult[i] = st.radio(q[0],['YES', 'NO'], horizontal=True, key = q[4])
			elif q[1] == 'numeric':
				catResult[i] = st.number_input(q[0], step = 1, key = q[4])

		st.expander('Help for Value for ' + category).write("HELP TEXT TODO")
	return (questions, catResult)



data = readExcel()
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
# Header
###################
cola, colb = st.columns([4,1])
with cola:
	st.title('WBDK Prioritising Tool v.1.0')
with colb:
	st.image('assets/logo.jpg')

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
for cat in catTypes:
	categoryWidget(cat, actType, importedData, keys)



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

