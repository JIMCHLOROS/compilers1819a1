"""
Sample script to test ad-hoc scanning by table drive.
This accepts a number with optional decimal part [0-9]+(\.[0-9]+)?

NOTE: suitable for optional matches
"""

def getchar(text,pos):
	""" returns char category at position `pos` of `text`,
	or None if out of bounds """
	
	if pos<0 or pos>=len(text): return None
	
	c = text[pos]
	
	# **Σημείο #3**: Προαιρετικά, προσθέστε τις δικές σας ομαδοποιήσεις
	if c=='0': return 'DIGIT_0'                  # 0
	if c>='1' and c<='2': return 'DIGIT_0-2'     # 1..2 grouped together
	if c=='3' : return 'DIGIT_3'                 # 3
	if c=='4': return 'DIGIT_4'                  # 4
	if c=='5': return 'DIGIT_5'                  # 5
	if c>='6' and c<='9': return 'DIGIT_6-9'     # 6..9 grouped together
	
	
	return c	# anything else
	


def scan(text,transitions,accepts):
	""" scans `text` while transitions exist in
	'transitions'. After that, if in a state belonging to
	`accepts`, it returns the corresponding token, else ERROR_TOKEN.
	"""
	
	# initial state
	pos = 0
	state = 's0'
	# memory for last seen accepting states
	last_token = None
	last_pos = None
	
	
	while True:
		
		c = getchar(text,pos)	# get next char (category)
		
		if state in transitions and c in transitions[state]:
			state = transitions[state][c]	# set new state
			pos += 1	# advance to next char
			
			# remember if current state is accepting
			if state in accepts:
				last_token = accepts[state]
				last_pos = pos
			
		else:	# no transition found

			if last_token is not None:	# if an accepting state already met
				return last_token,last_pos
			
			# else, no accepting state met yet
			return 'ERROR_TOKEN',pos
			
	
# **Σημείο #1**: Αντικαταστήστε με το δικό σας λεξικό μεταβάσεων
transitions = { 'q0': { 'DIGIT_0':'q1' , 'DIGIT_1-2':'q1','DIGIT_3':'q2' },
       		'q1': { 'DIGIT_0':'q4','DIGIT_1-2':'q4','DIGIT_3':'q4','DIGIT_4':'q4','DIGIT_5':'q4','DIGIT_6-9':'q4' },
       		'q2': { 'DIGIT_0':'q3','DIGIT_1-2':'q3','DIGIT_3':'q3','DIGIT_4':'q3','DIGIT_5':'q4' },
	        'q3': { 'DIGIT_0':'q5','DIGIT_1-2':'q5','DIGIT_3':'q5','DIGIT_4':'q5','DIGIT_5':'q5','DIGIT_6-9':'q5' },
	        'q4': { 'DIGIT_0':'q5'},
	        'q5': { 'DIGIT_0':'q6','DIGIT_1-2':'q6','DIGIT_3':'q6','DIGIT_4':'q6','DIGIT_5':'q6','DIGIT_6-9':'q6' },
	        'q6': { 'DIGIT_0':'q7','DIGIT_1-2':'q7','DIGIT_3':'q7','DIGIT_4':'q7','DIGIT_5':'q7','DIGIT_6-9':'q7'  },
	        'q7': { 'K':'q8' ,'G':'q9' ,'M':'q13' },
	        'q8': { 'T':'q12' },
	        'q9': { 'DIGIT_0':'q10','DIGIT_1-2':'q10','DIGIT_3':'q10','DIGIT_4':'q10','DIGIT_5':'q10','DIGIT_6-9':'q10' },
	        'q10': { 'DIGIT_0':'q11','DIGIT_1-2':'q11','DIGIT_3':'q11','DIGIT_4':'q11','DIGIT_5':'q11','DIGIT_6-9':'q11'},     
	        'q11': { 'K':'q8'},
	        'q13': { 'P':'q14' },
	        'q14': { 'S':'q15' },
     		  } 

# **Σημείο #2**: Αντικαταστήστε με το δικό σας λεξικό καταστάσεων αποδοχής
accepts = { 'q15':'WIND_TOKEN',
       	    'q12':'WIND_TOKEN'	
     	  }


# get a string from input
text = input('give some input>')

# scan text until no more input
while text:		# i.e. len(text)>0
	# get next token and position after last char recognized
	token,pos = scan(text,transitions,accepts)
	if token=='ERROR_TOKEN':
		print('unrecognized input at position',pos,'of',text)
		break
	print("token:",token,"text:",text[:pos])
	# new text for next scan
	text = text[pos:]
	
