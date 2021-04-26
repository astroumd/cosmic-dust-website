import pandas as pd
import openpyxl
import os
    
def load_data(in_file):
    #This function is ran whenever a new excel file is added to the database.
    #We need to specify the name of the file as an input argument.

    in_path = ''.join(['database/',in_file])
    df = pd.read_excel(in_path, engine="openpyxl")
    df = df.iloc[0:-1]

    mat = in_file.replace('.xlsx','')
    print(f"Mat is {mat}")
    
    #we are creating text files in the backend_database to be used by the C code.
    output_path = os.path.join('backend_database',mat)
    
    try:
        #This statement only runs correctly if we are adding a new material
        os.mkdir(output_path)
        #If we are adding a new material, we should add it to the material_list.
        with open("mat_list.txt", 'a') as mat_list:
            print(mat, file=mat_list)
    except (FileExistsError):
        print('directory exist')
    
    #now we are adding the .txt files within this directory
    output_path = ''.join([output_path,"/"])
    
    #The column names are different than the file names used in the C code.
    #Each index indicates a correct mapping from data column to .txt file name.
    col_names = ["S11_0.45", "Pol_0.45", "S11_0.65", "Pol_0.65"]
    out_file_names =["bright_0.45","pola_0.45","bright_0.65","pola_0.65"]

    #This loop creates each of the four .txt files.
    for idx,col in enumerate(col_names):
        new_out_path = ''.join([output_path,out_file_names[idx],'.txt'])
        data = df[col].values.tolist()
        row_list = [data[x:x+182] for x in range(0,len(data), 182)]
        with open(new_out_path, "w") as current_file:
            for row in row_list:
                row = row[0:-1]
                print(*row, sep =", ", file=current_file)

def check_files():
    #This function is ran whenever a calculator page is loaded.
    #It makes sure the excel files have cooresponding files in the backend_database.
    #The output is the list of valid inputs to become "form-select options" in the HTML forms
    mat_list = []
    with open('mat_list.txt', 'r') as data_log:
        for item in data_log:
            mat_list.append(item.replace('\n','')) 
    
    remaining_mats = mat_list.copy()
    
    path = r"database"
    for obj in os.listdir(path):
        if obj.replace('.xlsx','') in remaining_mats:
            remaining_mats.remove(obj.replace('.xlsx',''))
        else:
            print(f'new data. This file is {obj}')
            mat_list.append(obj.replace('.xlsx',''))
            load_data(obj)
    
    #If there are any entries in mat_list.txt without cooresponding files in the backend_database,
    #They should be removed.
    if len(remaining_mats) != 0:
        for item in remaining_mats:
            print(f"Removing {item}")
            mat_list.remove(item)
            with open("mat_list.txt", 'w') as new_mat_list:
                for new_mat in mat_list:
                    print(new_mat, file=new_mat_list)
    
    #this list contains the valid calculator inputs
    return sorted(mat_list)
            