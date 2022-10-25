import pandas as pd
import time
import requests
import wget
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "https://www.ine.cl/estadisticas/sociales/economia-regional/repositorio-de-estadisticas-regionales"

def getDriver(link):
    print("Vamos =) ")
    options = Options()
    print('A')
    options.log.level = "trace"
    print('B')
    options.add_argument("--headless")
    print('C')
    options.set_preference("browser.download.manager.showWhenStarting", False)
    print('D')
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    print('E')
    driver = webdriver.Firefox(options=options)
    print('F')
    driver.set_page_load_timeout("600")
    print('G')
    driver.get(link)
    print('Cargado')
    print('H')
    
    return driver

def descarga():
    
    urlGecko = "https://github.com/hectorflores329/gecko/blob/main/geckodriver.exe"
    wget.download(urlGecko, 'geckodriver.exe')

    time.sleep(30)

    print("Gecko driver descargado")

    web = 0
    # while(web == 0):
    try:
        driver = getDriver(url)
        time.sleep(30)
        web = 1
    except:
        # webdriver.Firefox()
        # driver.delete_all_cookies()

        print('Error al cargar la URL')

    print(1)

    time.sleep(30)

    information = driver.find_element_by_xpath("/html/body/form/div[8]/div[3]/div[1]/div/div/div/div[1]")
    information.click()
    time.sleep(5)

    print(2)

    files = driver.find_element_by_xpath("/html/body/form/div[8]/div[3]/div[2]/div/div/div/div[4]/div/div/div")
    files.click()
    time.sleep(5)

    _file1 = driver.find_element_by_xpath("/html/body/form/div[8]/div[3]/div[3]/div/div/div/div/div[2]/a[1]").get_attribute('href')
    time.sleep(5)

    print(3)

    _file2 = driver.find_element_by_xpath("/html/body/form/div[8]/div[3]/div[3]/div/div/div/div/div[2]/a[2]").get_attribute('href')
    time.sleep(5)

    print(4)

    dfHomologado = pd.read_excel('Estadísticas Regionales/Tabla_Homologacion.xlsx')

    print(5)

    def homologacion(cod):

        dfFiltrado = dfHomologado[dfHomologado["Código Variable"] == str(cod)]
        indx = dfFiltrado.index[0]

        glosa = dfFiltrado["Glosa Variable"][indx]
        return glosa

    try:
        filen1 = requests.get(_file1, allow_redirects=True)
        open('Estadísticas Regionales/estadísticas-regionales.xlsx', 'wb').write(filen1.content)
        print('Archivo estadísticas-regionales.xlsx descargado correctamente')

        try:
            df= pd.read_excel('Estadísticas Regionales/estadísticas-regionales.xlsx')
            
            time.sleep(2)
            df.columns = df.iloc[2]

            time.sleep(2)
            df = df.drop(range(3))

            time.sleep(2)

            df["Glosa Variable"] = df["Código Variable"].apply(lambda x: homologacion(x))

            df.to_excel('Estadísticas Regionales/estadísticas-regionales.xlsx', index=False)

            df_final_skip = pd.read_excel('Estadísticas Regionales/estadísticas-regionales.xlsx', skiprows=3)
            df_final_skip.to_excel('Estadísticas Regionales/estadísticas-regionales.xlsx', index=False)

            print('Proceso finalizado.')

        except:
            print("No se ha podido procesar el archivo.")

    except:
        print("No se ha podido descargar el archivo: estadísticas-regionales.xlsx")

    try:
        filen2 = requests.get(_file2, allow_redirects=True)
        open('Estadísticas Regionales/descriptor-de-campos.xlsx', 'wb').write(filen2.content)
        print('Archivo descriptor-de-campos.xlsx descargado correctamente')

    except:
        print('No se ha podido descargar el archivo: descriptor-de-campos.xlsx')

if __name__ == '__main__':
    descarga()