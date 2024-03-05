import pandas as pd
from os import listdir, mkdir
from os.path import isfile, join
import sys

# TODO: refactor and make this script more generic for reusability

path = r"G:\\My Drive\\SEDS\\assignment01\\data"

try:
    files = [f for f in listdir(path) if isfile(join(path, f))]
    print("[SUCCESS] fetched file list from directory: "+path)
except:
    print("[ERROR] Error finding files in directory: " + path)
    sys.exit(1)

outfile_name = 'fxgl_metrics'

try:
    outpath = path+'\\..\\out'
    mkdir(outpath)
    print("[SUCCESS] Created out directory: " + outpath)

except FileExistsError:
    print("[ERROR] Directory already exists: "+ outpath)
    print("[INFO] Continuing execution...")

except Exception as e:
    print("[ERROR] Error creating out directory: "+ outpath + e.message())
    sys.exit(1)


beeg_df_list = []
beeg_sheet_names_list = []

for f in files: 
    print("[INFO] performing operation on file")
    fxgl_metrics = pd.read_csv(path+'\\'+f)
    fxgl_metrics_int = fxgl_metrics[fxgl_metrics['Kind'].str.contains('Class')].drop('Kind', axis=1)
    fxgl_metrics_int = fxgl_metrics_int.rename(columns={'Name':'Class', 'CountLineCode':'LOC (Lines of Code)', 'PercentLackOfCohesion':'LCOM (Percent Lack of Cohesion)', 'MaxInheritanceTree':'DIT (Max Inheritance Tree)', 'CountClassBase':'IFANIN (Count of Base Classes)',  'CountClassCoupled':'CBO (Count of Coupled Classes)', 'CountClassDerived':'NOC (Count of Derived Classes)', 'CountDeclMethodAll':'RFC (Count of All Methods)', 'CountDeclMethod':'NIM (Count of Instance Methods)', 'CountDeclInstanceVariable':'NIV (Count of Instance Variables)', 'CountDeclInstanceMethod':'WMC (Count of Methods)', 'MaxCyclomatic':'MC (Max Cyclomatic)'})
    beeg_df_list.append(fxgl_metrics_int[['Class', 'LOC (Lines of Code)', 'LCOM (Percent Lack of Cohesion)', 'DIT (Max Inheritance Tree)', 'IFANIN (Count of Base Classes)', 'CBO (Count of Coupled Classes)', 'NOC (Count of Derived Classes)', 'RFC (Count of All Methods)', 'NIM (Count of Instance Methods)', 'NIV (Count of Instance Variables)', 'WMC (Count of Methods)', 'MC (Max Cyclomatic)']])
    beeg_sheet_names_list.append('.'.join(f.split('.')[:-1]))

with pd.ExcelWriter(outpath+"\\"+outfile_name+'.xlsx') as writer:
    for df, df_sheet_name in zip(beeg_df_list, beeg_sheet_names_list):
        df.to_excel(writer, sheet_name = df_sheet_name, index=False)

print("[INFO] Operation completed")

