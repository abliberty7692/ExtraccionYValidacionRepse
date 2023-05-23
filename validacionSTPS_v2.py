from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from random import randrange, choice
import time
import pandas as pd
import re
from argparse import ArgumentParser
from fake_useragent import UserAgent
import math

user_agents_list = ["Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.3",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36",
"Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36"]

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

len_lst_razon_social = len(lst_razon_social)
pages = math.floor(len_lst_razon_social/100)
pages = 1 if not pages else pages

for i in range(pages):
    print(f"####[Page: {i}]")
    lst_razon_social_paginada = lst_razon_social[i*100:(i+1)*100] \
        if not i == pages-1 else lst_razon_social[i*100:len_lst_razon_social]

    #5.
    #ua = UserAgent(browsers=['chrome'])
    #userAgent = ua.random
    #print(userAgent)
    #options.add_argument(f'user-agent={userAgent}')
    options = Options()
    #options.add_argument("--headless")
    #options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument(f'user-agent={choice(user_agents_list)}')

    driver = webdriver.Chrome(options=options)
    #driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": choice(user_agents_list)}) 
    #driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 

    #stealth(driver,
    #    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.105 Safari/537.36',\
    #    languages=["es-MX", "es"],\
    #    vendor="Google Inc.",\
    #    platform="Win32",\
    #    webgl_vendor="Intel Inc.",\
    #    renderer="Intel Iris OpenGL Engine",\
    #    fix_hairline=True,\
    #    )
    #driver = webdriver.Chrome()
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
    bloqueado_por_captcha = False
    for razon_social, j in zip(lst_razon_social_paginada, range(len(lst_razon_social_paginada))):
        if j%50 == 0: time.sleep(randrange(10,15))
        try:
            print(f">>>>>>>>>>>>[#{j}]{razon_social}")
            #7.1
            if(not razon_social):
                lst_repses_vigentes.append(False)
                continue

            #7.2
            search_input = driver.find_element(By.ID, "rsoc").clear()
            search_input = driver.find_element(By.ID, "rsoc").send_keys(razon_social)
            time.sleep(randrange(5,8)/10)
            search_button = driver.find_element(By.ID, "bnt_busqueda")
            search_button.click()
            time.sleep(randrange(24, 28)/10)

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
                print(f'[Estatus]{razon_social in source_code}')
            #7.5.1
            else:
                lst_repses_vigentes.append("Revision")
                revision_conteo+=1

            #print(lst_repses_vigentes[-1])
            #print(razon_social in source_code)
            #7.6
            if(revision_conteo==10):
                revision_conteo=0
                bloqueado_por_captcha = True
                break
            time.sleep(1)
        except:
            #7.5.4
            lst_repses_vigentes.append("Error")

    driver.quit()
    if(bloqueado_por_captcha): break

#print(table)

# #8.
for registro, vigencia in zip(table, lst_repses_vigentes):
    registro.append(vigencia)

#os.remove(path_lst_repse)

#9.
df = pd.DataFrame(table)#, columns=column_names)
df.columns = ['RFC', 'REPSE', 'Razon Social', 'FECHA', 'Descripcion', 'Documento', 'Vigente']
df.to_excel(path_lst_repse[:-4]+"_validado.xlsx", index=False, encoding='latin1')