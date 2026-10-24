import logging
import csv,json
from pathlib import Path

desktop_dir=Path.home()/"Desktop"
log_file = desktop_dir/"file_Generator.log"
csv_file  = desktop_dir/"users.csv"
json_file = desktop_dir/"users.json"

logging.basicConfig( 
    filename =log_file,
    level=logging.DEBUG,
    format='%(asctime)s- %(levelname)s - %(message)s',
    filemode= 'w',
    force  =  True 
)
logging.info("Starting the file generation process...")

csv_data =[
    ["Name","Age","City"],
    ["Rana",35,"Aayodhya"],
    ["Rajan",28,"North East delhi"],
    ["Geeta Rana ",22,"Gurugram"]
]

json_data  =[
    {"Name":"Ram","Age":25,"City":"Agra"},
    {"Name":"Raman","Age":26,"City":"Delhi"},
    {"Name":"Geeta","Age":22,"City":"Gurugram"}
]

try:
    logging.debug(f"Attempting to conect to the database and to create CSV at :{csv_file}.")
    with open(csv_file,'w',newline="\n", encoding='utf-8') as f:
        writer=csv.writer(f)#,fieldnames = fieldnames)
        writer.writerows(csv_data)
    logging.info("CSV file created successfully.")
    print(csv_file)
    #print(csv_data)
except Exception as e :  
    logging.error(f"Failed to create CSV file.An eror occurred :{e}")
   
try:
    logging.debug(f"Attempting  to  conect to the database and and to create JSON at :{json_file}")
    with open(json_file,'w',newline="\n", encoding='utf-8') as file:
        json.dump(json_data,file,indent=4)
    logging.info("JSON file created successfully.")
    print(json_file)
    #print(json_data)
except Exception as e :  
    logging.error(f"Failed to create JSON file.An eror occurred :{e}")
logging.info("Process finished successfully.")
print("Script executed,check your files !")
    