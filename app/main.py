from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from flask import render_template
# from app import app
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
	vari = map(lambda x:x.lower(),vari)
	key_list = []
	stem_list = []
	path = os.getcwd()+"/templates/file_storage"
	for k in range(len(vari)):
		file_list = []
		for file in os.listdir(path):
			

			if file.endswith(".txt"):
				# path = '/var/www/html/filesearch/file_storage/%s' %(file)
				path_file = path+'/'+file
				fo = open(path_file,'r')
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

@app.route('/file1')
def file_one():
	return render_template("file_storage/Dear_John.txt")

@app.route('/file2')
def file_two():
	return render_template("file_storage/a_walk_to_remember.txt")

@app.route('/file3')
def file_three():
	return render_template("file_storage/the_last_song.txt")

@app.route('/file4')
def file_four():
	return render_template("file_storage/the_notebook.txt")

