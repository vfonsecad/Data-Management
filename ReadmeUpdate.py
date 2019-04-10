# ----------------------------------------------------------------------

# -------------------------- README UPDATE PROGRAM -------------------

# ----------------------------------------------------------------------

# --- readme update
import os

current_folder = os.getcwd()
file_in = current_folder + "/readme.txt"
with open(file_in) as f:
    file_content = f.readlines()
lines_content = [line.replace("\n","").split(";") for line in file_content if not("FOLDER_ID" in line or "file_name" in line or line=="\n")]
name_in_readme = sorted([x[0] for x in lines_content])
name_in_corefolder = sorted([f for f in os.listdir(current_folder) if (not f.startswith(".") and not f.startswith("_"))])
name_in_corefolder.remove("readme.txt")

# Conditions to check
if not(name_in_corefolder == name_in_readme):
    not_in_readme = [x for x in name_in_corefolder if x not in name_in_readme]
    if len(not_in_readme)>0:
        for fx in not_in_readme:
            print(fx + ";")
else:
    print("\n\n ------- no update needed ---------\n\n ")
