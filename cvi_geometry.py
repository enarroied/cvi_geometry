from decimal import Decimal
import tabula
import csv
import os

#Defie global empty data sets for further appending
cvi_number = ""
lieudit_list = []
insee_code_list = []
product_list = []
variety_list = []
area_list = []
year_list = []
density_list = []

def get_parcel(file, output_file, output_file_fail) :
    tabula.convert_into(file, "buffer.csv", lattice=True, output_format="csv", pages='all')
    with open('buffer.csv', 'r') as bufferfile: 
        reader = csv.reader(bufferfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[-1] == "Arrachage" :
                continue
            elif row[0] == "Numéro CVI" :
                global cvi_number
                cvi_number = row[1]
            try :
                if "-" in row[7] :
                    insee_code = row[1][:2] + row[1][3:6] + "000" + row[1][-6:]
                    insee_code = insee_code.replace(' ', '0')
                    #Density = 10000 m2 / (width[cm]/100 * length[cm]/100) --> 100000000 /(width * length)
                    density = int(100000000/ (int(row[9]) * int(row[10]) ) )
                    #Area is hectares (ha)
                    area = float(row[4]) + float(row[5])/100 + float(row[6])/10000
                    area = Decimal(area).quantize(Decimal('1e-4'))
                    #Append data to lists
                    #Also remove newlines that may be in the original pdf file
                    lieudit_list.append(row[0].replace('\n', ' '))
                    insee_code_list.append(insee_code)
                    product_list.append(row[2].replace('\n', ' '))
                    variety_list.append(row[3].replace('\n', ' '))
                    area_list.append(area)
                    year_list.append(row[7].replace('\n', ' '))
                    density_list.append(density)
            except :
                continue
    bufferfile.close()
    #Write output and check for all the land registry files in the CADASTRE folder
    for registry_file in os.listdir('./CADASTRE') :
        if registry_file[-5:] == ".json" :
            registry_file_path = f'./CADASTRE/{registry_file}'
            write_output(registry_file_path, output_file)
        else :
            continue
    write_output_fail(output_file_fail)
    os.remove("buffer.csv")

def write_output(registry_file, output_file) :
    global insee_code_list, cvi_number, lieudit_list, product_list, variety_list, area_list, year_list, density_list
    with open(registry_file, 'r+') as registry_file, open(output_file, 'a+') as output:
        for registry in registry_file :
            index_list = []
            for index, insee in enumerate(insee_code_list) :
                if f'"id":"{insee}' in registry :
                    #extract geometry with pure python and return a WKT format
                    geometry = registry.split('"coordinates":[[[')[1]
                    geometry = geometry.split(']]]}')[0]
                    geometry = geometry.replace(',', ' ')
                    geometry = geometry.replace('] [', ',')
                    geometry = '"POLYGON ((' + geometry + '))"'
                    index_list.append(index)
                    output.write(f"{geometry}, {cvi_number}, {lieudit_list[index]}, {insee}, {product_list[index]}, {variety_list[index]}, {area_list[index]}, {year_list[index]}, {density_list[index]}\n")
            index_list.sort()
            for count, index in enumerate(index_list) :
                index_pop = index - count
                insee_code_list.pop(index_pop)
                lieudit_list.pop(index_pop)
                product_list.pop(index_pop)
                variety_list.pop(index_pop)
                area_list.pop(index_pop)
                year_list.pop(index_pop)
                density_list.pop(index_pop)

    registry_file.close()
    output.close()

def write_output_fail(output_file_fail) :
    global insee_code_list, cvi_number, lieudit_list, product_list, variety_list, area_list, year_list, density_list
    with open(output_file_fail, 'a+') as fail :
        for index, insee in enumerate(insee_code_list) :
            fail.write(f'{insee}, {cvi_number}, {lieudit_list[index]}, {product_list[index]}, {variety_list[index]}, {area_list[index]}, {year_list[index]}, {density_list[index]}\n')
    insee_code_list=[]
    lieudit_list=[]
    product_list=[]
    variety_list=[]
    area_list=[]
    year_list=[]
    density_list=[]
    fail.close()



##########################################
##   Enter name of output files below   ##
##########################################
output_file = "output.csv"
output_file_fail = "output_fail.csv"
##########################################

# Create the header of the output file
with open(output_file, 'w+') as output, open(output_file_fail, 'w+') as output_fail :
    output.write('WKT, Numéro CVI, Lieu-Dit, Code INSEE, Produit, Cépage, Surface (ha), Campagne Plantation, Densité\n')
    output_fail.write('code Insee, Numéro CVI, Lieu-Dit, Produit, Cépage, Surface (ha), Campagne Plantation, Densité\n')
output.close()

for cvi_filename in os.listdir('./cvis') :
    if cvi_filename == "README.txt" : continue
    cvi_filepath = f"./cvis/{cvi_filename}"
    get_parcel(cvi_filepath, output_file, output_file_fail)
