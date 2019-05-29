# ----------------------------------------------------------------------

# -------------------------- DATA MANAGEMENT PROGRAM -------------------

# ----------------------------------------------------------------------



# --- Imports

import os
import datetime


# --- Home directory

homedir = '/home/valeria/vfonsecad/kul_phd'

# --- Get current date

date_now = datetime.datetime.now()
if date_now.month < 10:
    month = "0" + str(date_now.month)
else:
    month = str(date_now.month)

today = str(date_now.year) + "_" + month + "_" +  str(date_now.day)


# --- Get all  core folders (i.e that will be assigned an ID)

core_folders=list()
for root, dirs, files in os.walk(homedir + '/programming'):
    current_list = [root, dirs, files]
    if 'readme.txt' in current_list[2]:
        core_folders.append(current_list)

core_folders_path = [x[0] for x in core_folders]

# --- Get folders that should have readme and dont have it


core_folders_noreadme = list()


for root, dirs, files in os.walk(homedir + '/programming'):
    
    if "LIBRA_20160628" not in root:
                
        files = [x for x in files if not x.startswith(".") and not x.startswith("_")]
        if len(files)>0 and "readme.txt" not in files and "diary-experiment.txt" not in files and "/." not in root and "/_" not in root:
            if sum([x in root for x in core_folders_path])==0:
                core_folders_noreadme.append(root)


# --- Correct FOLDER_ID line and first line after description


for core_folder in core_folders:
    file_in = core_folder[0] + "/readme.txt"
    f = open(file_in, "r")
    lines = f.readlines()
    f.close()
    f = open(file_in, "w")
    for line in lines:
        line_list = line.split(";")
        if "FOLDER_ID" in line_list and len(line_list)==2:
            f.write(line + ";\n")
        if "file_name" in line_list and len(line_list)==2:
            f.write(line_list[0] + ";description;\n")
        elif not(len(line_list) == 1 or line == ";\n"):
            f.write(line)

    f.close()



# --- Core folders with no FOLDER_ID

core_folders_new = list()
for core_folder in core_folders:
    file_in = core_folder[0] + "/readme.txt"
    with open(file_in) as f:
        content = f.readlines()
        add = "FOLDER_ID" not in [line.split(";")[0] for line in content]
        if add:
            core_folders_new.append(core_folder)




# --- Assign ID to new core folders

kk = 1
base_id = "0000"
for core_folder in core_folders_new:
    file_in = core_folder[0] + "/readme.txt"
    current_ID = today + "_" + base_id[0:(4-len(str(kk)))] + str(kk)
    kk += 1
    with open(file_in, "a") as f:
        f.write("\nFOLDER_ID;"+current_ID+";\n")

# --- Update compilation of core folders id

file_CoreFolders_txt = open(homedir + "/data-management-system/info-files/core-folders.txt", "r")
CoreFolders_txt_lines = file_CoreFolders_txt.readlines()
file_CoreFolders_txt.close()
all_ids = [line.split(";")[0] for line in CoreFolders_txt_lines] ## All current id's
file_CoreFolders_txt = open(homedir + "/data-management-system/info-files/core-folders.txt", "w")
file_CoreFolders_txt.write("FOLDER_ID;FOLDER_PATH;FOLDER_DESCRIPTION;FOLDER_MODIFICATIONS;\n")

for core_folder in core_folders:
    file_in = core_folder[0] + "/readme.txt"

    with open(file_in) as f:
        file_content = f.readlines()
        core_folder_id = [line.split(";")[1] for line in file_content if "FOLDER_ID" in line][0]
        description = [line.split(";")[2] for line in file_content if "file_name" in line]


        if core_folder_id in all_ids:
            line_id = all_ids.index(core_folder_id)
            line_components = CoreFolders_txt_lines[line_id].split(";")
            if core_folder[0]!=line_components[1]:
                n_modifications = int(line_components[3])+1
            else:
                n_modifications = int(line_components[3])
            line_update = core_folder_id + ";" + core_folder[0] + ";" + description[0].split("\n")[0] +";" +str(n_modifications) + ";\n"
        else:
            line_update = core_folder_id +";" + core_folder[0] + ";" + description[0].split("\n")[0] +";" +"0" + ";\n"

        file_CoreFolders_txt.write(line_update)

file_CoreFolders_txt.close()


# --- Verify that all core folders have a well defined readme.txt file

log_txt = open(homedir + "/data-management-system/info-files/log.txt", "w")

for core_folder in core_folders:
    file_in = core_folder[0] + "/readme.txt"
    with open(file_in) as f:
        file_content = f.readlines()
    lines_content = [line.replace("\n","").split(";") for line in file_content if not("FOLDER_ID" in line or "file_name" in line or line=="\n")]
    name_in_readme = sorted([x[0] for x in lines_content])
    descrip_in_readme = [len(x[1])>2 for x in lines_content if len(x)>1]
    name_in_corefolder = sorted([f for f in os.listdir(core_folder[0]) if (not f.startswith(".") and not f.startswith("_"))])
    name_in_corefolder.remove("readme.txt")
    # Conditions to check
    if not(name_in_corefolder == name_in_readme):
        wrong_in_readme = [x for x in name_in_corefolder if x not in name_in_readme]
        wrong_in_corefolder = [x for x in name_in_readme if x not in name_in_corefolder]        
        log_txt.write(core_folder[0] + "; Files in readme not the same as files in core folder\n")
        log_txt.write("-- Files in readme NOT in core folder: " + " -- ".join(wrong_in_corefolder) + "\n")
        log_txt.write("-- Files in core folder NOT in readme: " + " -- ".join(wrong_in_readme) + "\n")
    if sum(descrip_in_readme)!=len(name_in_readme):
        log_txt.write(core_folder[0] + "; Not all files contain description\n")
    # --- Checking error of cor folders are folders of another core folder
    for ic in range(0,len(core_folder[1])):
        current_folder = core_folder[0]+"/"+core_folder[1][ic]
        for root, dirs, files in os.walk(current_folder):
            current_list = [root, dirs, files]
            if 'readme.txt' in current_list[2]:
                log_txt.write(core_folder[0] + "; Found Core folder as subfolder of another core folder \n")
    
log_txt.write("\n\n\n\n\n----------------- FOLDERS WITH NO readme.txt ---------------------\n\n")
                
for core_folder in core_folders_noreadme:    
    log_txt.write(core_folder + "\n\n")
                
log_txt.write("\n\n\n\n\n-----------------Process finished--------------------\n\n")
log_txt.close()
