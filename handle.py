import chardet
import json 

#Step2: Detect the Encoding 
with open('db_leavesystem.json', 'rb') as file:
	result = chardet.detect(file.read()) 
	encoding = result['encoding'] 
	print(f"Detected Encoding: {encoding}") 
	
#Step3: Load file with correct encoding and optionally re-encoding to UTF-8 
with open('db_leavesystem.json', 'r' , encoding = encoding) as file:
	data = json.load(file) 
		
#optionally save the data in the utf-8 encoding 
with open('db_leavesystem_postgres.json', 'w', encoding= 'utf-8') as file:
	json.dump(data, file)
		