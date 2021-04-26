import csv

table_header = []
table_data = []
with open('outfile.csv', newline='') as output_file:
    csv_data = csv.reader(output_file, delimiter=" ")
    for idx,row in enumerate(csv_data):
        if idx <=3:
            table_header.append(row)
        else:
            table_data.append(row)
print(f'Header is {table_header}')

print(f'Data  is {table_data}')