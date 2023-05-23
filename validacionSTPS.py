from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
from argparse import ArgumentParser

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s
#1.
parser = ArgumentParser()
parser.add_argument("-p", "--path", help="Path to the csv file to read")
args = parser.parse_args()
path_lst_repse = args.path

#2.
ws = pd.read_csv(path_lst_repse, sep=',', encoding='latin1')
#3.
table = ws.values.tolist()
lst_razon_social = []

#4.
for e in table:
    try:
        lst_razon_social.append(normalize(re.sub(" +"," ",e[2].upper().replace(".", "").replace(",", "").replace(" SA DE CV", "").strip())))
    except:
        lst_razon_social.append("")
        

lst_repses_vigentes = []

#5.
driver = webdriver.Chrome()
driver.get("https://repse.stps.gob.mx/")
driver.maximize_window()
time.sleep(10)

#6.
button = driver.find_element(By.ID, "act-consulta")
button.click()
time.sleep(5)

button2 = driver.find_element(By.CSS_SELECTOR, ".btn-continue")
button2.click()
time.sleep(10)

#7.
revision_conteo = 0
for razon_social in lst_razon_social:
    try:
        print(">>>>>>>>>>>>"+razon_social)
        #7.1
        if(not razon_social):
            lst_repses_vigentes.append(False)
            continue

        #7.2
        search_input = driver.find_element(By.ID, "rsoc").clear()
        search_input = driver.find_element(By.ID, "rsoc").send_keys(razon_social)
        time.sleep(0.1)
        search_button = driver.find_element(By.ID, "bnt_busqueda")
        search_button.click()
        time.sleep(2)

        #7.3
        source_code = driver.page_source.replace("&amp;", "&")
        #7.4
        while not (razon_social in source_code or 'No hay datos' in source_code or 'capcha incorrecta' in source_code):
            time.sleep(1)
            source_code = driver.page_source.replace("&amp;", "&")

        #7.5
        #7.5.2 & 7.5.3
        if not "capcha incorrecta" in source_code:
            lst_repses_vigentes.append(razon_social in source_code)
        #7.5.1
        else:
            lst_repses_vigentes.append("Revision")
            revision_conteo+=1

        print(lst_repses_vigentes[-1])
        #print(razon_social in source_code)
        #7.6
        if(revision_conteo==10):
            revision_conteo=0
            break
        time.sleep(1)
    except:
        #7.5.4
        lst_repses_vigentes.append("Error")

print(table)

#8.
for registro, vigencia in zip(table, lst_repses_vigentes):
    registro.append(vigencia)

#os.remove(path_lst_repse)

#9.
df = pd.DataFrame(table)#, columns=column_names)
df.columns = ['RFC', 'REPSE', 'Razon Social', 'FECHA', 'Descripcion', 'Documento', 'Vigente']
df.to_excel(path_lst_repse[:-4]+"_validado.xlsx", index=False, encoding='latin1')