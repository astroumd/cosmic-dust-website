#To run this script from the terminal:
# 1) enter the virtual enviorment with the command: "source bin/activate"
# 2) "export FLASK_APP=app.py"
# 3) "export FLASK_ENV=development"
# 4) "flask run"

# 3) is called so that changes to this script are automatically pushed to the site.
###########

#By default, @app.route() only accept HTTP get request.
#Use the methods argument to add other options.
#ex: app.route('/login',methods=['GET', 'POST'])
#    def login():
#        if request.method == 'POST':
#           return login_function()
#        else:
#            return other_function()

from flask import Flask, render_template,request,send_file
import subprocess
import csv
import fileConverter

app = Flask(__name__)

#I will be adding a new form page for each of the possible calculations.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/polarization')
def polarization_form():
    mat_list = fileConverter.check_files()
    return render_template('polarization_form.html',mat_list=mat_list)

@app.route('/polarization_1')
def polarization1_form():
    mat_list = fileConverter.check_files()
    return render_template('polarization1_form.html',mat_list=mat_list)

@app.route('/brightness')
def brightness_form():
    mat_list = fileConverter.check_files()
    return render_template('brightness_form.html',mat_list=mat_list)

@app.route('/brightness_1')
def brightness1_form():
    mat_list = fileConverter.check_files()
    return render_template('brightness1_form.html',mat_list=mat_list)

@app.route('/size')
def size_form():
    mat_list = fileConverter.check_files()
    return render_template('size_form.html')

@app.route('/color')
def color_form():
    mat_list = fileConverter.check_files()
    return render_template('color_form.html',mat_list=mat_list)

@app.route('/color_1')
def color1_form():
    mat_list = fileConverter.check_files()
    return render_template('color1_form.html',mat_list=mat_list)

@app.route('/calculation', methods = ['POST', 'GET'])
def calculation():
    
    command_list = ['sudo ./calc_c']
    
    if request.method == 'GET':
        return 'bad request'
    if request.method == 'POST':        
        form_data = request.form
        
        for idx,item in enumerate(form_data):
            param = form_data.get(item)
            if item == 'step_in_ratio':
                param = str(int(param)/100)
            command_list.append(param)
            if idx ==0:
                #This will be used to determine how the data in output.csv should be processed.
                c_calc_function = (form_data.get(item),len(form_data)+1)
        
        #logic for reordering list elements to match c code.
        polar2_order = [0,1,2,3,6,7,4,5,8]
        if c_calc_function == ('find_pola', 9):
            command_list = [command_list[i] for i in polar2_order]
         
        #Building the command and calling it
        command = " ".join(command_list)
        print('from list')
        print(command)
        
        print(f"Function: {c_calc_function}")
        
        #see an older version (main.py) for how this command is constructed
        subprocess.run(command,shell=True) 
        #running this should create/update "output.csv"
        with open('outfile.csv', newline='') as output_file:
            csv_data = csv.reader(output_file, delimiter=",")
            table_header = []
            table_data = []
            if c_calc_function[1] in  (8,9):
                for idx, row in enumerate(csv_data):
                    if idx <4:
                        table_header.append(row)
                    if idx >=4:
                        table_data.append(row)
            if c_calc_function[1] == 5:
                for idx, row in enumerate(csv_data):
                    if idx <1:
                        table_header.append(row)
                    if idx >=1:
                        table_data.append(row)
            if c_calc_function[1] == 6:
                for idx, row in enumerate(csv_data):
                    if idx <1:
                        table_header.append(row)
                    if idx >=1:
                        table_data.append(row[0:-2])
            
        #now we need to read output.csv and input data to output
            return render_template('calculation_output.html',table_header = table_header, table_data = table_data)
        
        #The file dynamic_output_style.py has the improved method of formatting data to be sent to the HTML tempelate.
        #We will use some logic to determine how many rows from the top are part of the header.
        #First I would like to create a page for each of the calculations.

@app.route('/calculation/download/<file_path>')
def download (file_path = None):
    if file_path is None:
        self.Error(400)
    try:
        return send_file(file_path, as_attachment=True)
    except:
        self.Error(400)

@app.route('/documentation')
def documentation():
    return render_template('documentation_page.html')

@app.route('/documentation/materials')
def mat_docs():
    return render_template('documentation_materials.html')

@app.route('/documentation/color')
def color_docs():
    return render_template('documentation_color.html')

@app.route('/documentation/size')
def size_docs():
    return render_template('documentation_size.html')
