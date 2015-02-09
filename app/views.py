from flask import render_template
from app import app
import os
import json
import re
from flask import request
from whoosh.lang.morph_en import variations
from flask import jsonify 

@app.route('/')
def my_form():
    return render_template("index.html")
@app.route('/jsondata',methods=['GET','POST'])
def jsondata():
    

	keyword = request.form['text']
	vari = list(variations(keyword))
	print vari
	key_list = []
	stem_list = []

	for k in range(len(vari)):
		file_list = []
		for file in os.listdir("/var/www/html/filesearch/file_storage/"):
			

			if file.endswith(".txt"):
				path = '/var/www/html/filesearch/file_storage/%s' %(file)
				fo = open(path,'rb+')
		        line = fo.read()
		        line = line.lower()
		        line = re.sub('[!@#$".(),\']', '', line)
		        
		        freq = []
		        if vari[k] in line:

			        lines = line.splitlines()
			        no_of_lines = len(lines)
			        word_count = 0
			        
			        for i in range(no_of_lines):
			        	select_line = lines[i].split()
			        	enum = list(enumerate(select_line,1))

			        	for j in range(len(enum)):
			        		if enum[j][1] == vari[k]:
			        			word_count = word_count+1
			        freq.append(dict({"name":word_count,"parent":file}))
				file_list.append(dict({"name":file,"parent":file,"children":freq}))	

		stem_list.append(dict({"name":vari[k],"parent":file,"children":file_list}))

	key_list.append(dict({"name":keyword,"parent":"null","children":stem_list}))
	

	return render_template('d3.html',result = json.dumps(key_list))