
from openpyxl import load_workbook
import pandas as pd
import numpy as np
import os
if os.path.exists("cookieweb\\cookiejs2team.xlsx"):
    writer = pd.read_excel("cookieweb\\cookiejs2team.xlsx") 
    user_id = [i[0] for i in writer.values]
    cookie = [i[1] for i in writer.values]
else:
    user_id = []
    cookie = []
user_id += ['Spark','Pandas','Java','Python', 'PHP']
cookie += [25000,20000,15000,15000,18000]
columns=['user_id','Cookie']
df = pd.DataFrame(list(zip(user_id,cookie)), columns=columns)
with pd.ExcelWriter("cookieweb\\cookiejs2team.xlsx", engine='xlsxwriter', engine_kwargs={'options':{'strings_to_urls': False}}) as writer:
            df.to_excel(writer, sheet_name='cookie', index=False)