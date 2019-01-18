# ----------------------------------------------------------------------

# -------------------------- DATA MANAGEMENT PROGRAM -------------------

# ----------------------------------------------------------------------



# --- Imports

import os
import datetime


# --- Get current date

date_now = datetime.datetime.now()
if date_now.month < 10:
    month = "0" + str(date_now.month)
else:
    month = str(date_now.month)

today = str(date_now.year)[-2:] + "_" + month + "_" +  str(date_now.day)


# --- Get all  core folders (i.e that will be assigned an ID)

core_folders=list()
for root, dirs, files in os.walk('D:\Google Drive\KUL PhD\Programming'):
    current_list = [root, dirs, files]
    if 'readme.txt' in current_list[2]:
        core_folders.append(current_list)


# --- Correct FOLDER_ID line and first line after description


for core_folder in core_folders:
    file_in = core_folder[0] + "\\readme.txt"
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
    file_in = core_folder[0] + "\\readme.txt"
    with open(file_in) as f:
        content = f.readlines()
        add = "FOLDER_ID" not in [line.split(";")[0] for line in content]
        if add:
            core_folders_new.append(core_folder)




# --- Assign ID to new core folders

kk = 1
base_id = "0000"
for core_folder in core_folders_new:
    file_in = core_folder[0] + "\\readme.txt"
    current_ID = "19_01_17_"+ base_id[0:(4-len(str(kk)))] + str(kk)
    kk += 1
    with open(file_in, "a") as f:
        f.write("\nFOLDER_ID;"+current_ID+";\n")

# --- Update compilation of core folders id

file_CoreFolders_txt = open("D:\\Google Drive\\KUL PhD\\DataManagementSystem\\InfoFiles\\CoreFolders.txt", "r")
CoreFolders_txt_lines = file_CoreFolders_txt.readlines()
file_CoreFolders_txt.close()
all_ids = [line.split(";")[0] for line in CoreFolders_txt_lines] ## All current id's
file_CoreFolders_txt = open("D:\\Google Drive\\KUL PhD\\DataManagementSystem\\InfoFiles\\CoreFolders.txt", "w")
file_CoreFolders_txt.write("FOLDER_ID;FOLDER_PATH;FOLDER_DESCRIPTION;FOLDER_MODIFICATIONS;\n")

for core_folder in core_folders:
    file_in = core_folder[0] + "\\readme.txt"

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
            line_update = core_folder_id + ";" + core_folder[0] + ";" + line_components[2] +";" +str(n_modifications) + ";\n"
        else:
            line_update = core_folder_id +";" + core_folder[0] + ";" + description[0].split("\n")[0] +";" +"0" + ";\n"

        file_CoreFolders_txt.write(line_update)

file_CoreFolders_txt.close()


# --- Verify that all core folders have a well defined readme.txt file

for core_folder in core_folders[0:1]:
    file_in = core_folder[0] + "\\readme.txt"
    with open(file_in) as f:
        file_content = f.readlines()
        files_in_readme = [[line.split(";")[0], len(line.split(";"))] for line in file_content if not("FOLDER_ID" in line or "file_name" in line)]



