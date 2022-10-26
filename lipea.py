#!/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse
import sys
import os


ORG = {'0': 'Ailuropoda melanoleuca (giant panda)',
       '1': 'Apis mellifera (honey bee)',
       '10': 'Danio rerio (zebrafish)',
       '11': 'Drosophila melanogaster (fruit fly)',
       '12': 'Equus caballus (horse)',
       '13': 'Felis catus (domestic cat)',
       '14': 'Gallus gallus (chicken)',
       '15': 'Gekko japonicus',
       '16': 'Glycine max (soybean)',
       '17': 'Homo sapiens (human)',
       '18': 'Macaca mulatta (rhesus monkey)',
       '19': 'Mus musculus (mouse)',
       '2': 'Arabidopsis thaliana (thale cress)',
       '20': 'Musca domestica (house fly)',
       '21': 'Nicotiana tabacum (common tobacco)',
       '22': 'Olea europaea var. sylvestris (wild olive)',
       '23': 'Oryctolagus cuniculus (rabbit)',
       '24': 'Oryza sativa japonica (Japanese rice)',
       '25': 'Pan troglodytes (chimpanzee)',
       '26': 'Phaseolus vulgaris (common bean)',
       '27': 'Pongo abelii (Sumatran orangutan)',
       '28': 'Rattus norvegicus (rat)',
       '29': 'Saccharomyces cerevisiae (budding yeast)',
       '3': 'Balaenoptera acutorostrata scammoni (minke whale)',
       '30': 'Salmo salar (Atlantic salmon)',
       '31': 'Sus scrofa (pig)',
       '32': 'Taeniopygia guttata (zebra finch)',
       '33': 'Theobroma cacao (cacao)',
       '34': 'Vitis vinifera (wine grape)',
       '35': 'Xenopus tropicalis (western clawed frog)',
       '36': 'Zea mays (maize)',
       '4': 'Bos taurus (cow)',
       '5': 'Caenorhabditis elegans (nematode)',
       '6': 'Camelina sativa (false flax)',
       '7': 'Canis familiaris (dog)',
       '8': 'Capra hircus (goat)',
       '9': 'Cicer arietinum (chickpea)'}


def parse_input(input_text):
    f = open(input_text, "r", encoding="utf-8").read()
    return f


def parse_orgcode(org_list_path):
    f = open(org_list_path, "r", encoding="utf-8").readlines()[:]
    result = {str(index): org.strip() for index, org in enumerate(f)}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="这个程序完成Lipea自动化分析")
    parser.add_argument("-input", action="store", default="", dest="input_path", help="需要分析的列表",
                        )
    parser.add_argument("-org", action="store", default="", dest="orgcode", help="对应的物种编号（从0开始）",
                        )
    p = parser.parse_args()
    if p.input_path == '':
        parser.print_help()
        for i in range(len(ORG)):
            print(f"{i}\t{ORG[str(i)]}")
        sys.exit(1)
    os.system("rm ~/Downloads/*lipea_results*")
    url = "https://lipea.biotec.tu-dresden.de/analyze"
    input_path = os.path.join(os.getcwd(),p.input_path)
    # 初始化并提交脂质列表。Step1
    browser = webdriver.Chrome()
    # browser.set_window_size(600,600)
    wait = WebDriverWait(browser, 100)
    input_text = parse_input(input_path)
    browser.get(url)

    text_box = browser.find_element(By.ID, "corebundle_analysis_lipidsList")
    text_box.send_keys(input_text)
    botton1 = browser.find_element(By.XPATH, '//*[@id="wizardProperty"]/div/div[1]/button[1]')
    botton1.click()
    # Step2
    Background_provider = browser.find_element(By.ID, "corebundle_analysis_backgroundProvider")
    organism = browser.find_element(By.ID, "corebundle_analysis_idOrganism")
    Select(Background_provider).select_by_index(1)
    Select(organism).select_by_index(int(p.orgcode))
    botton2 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wizardProperty"]/div/div[1]/button[1]')))
    botton2.click()
    # Step3
    botton3 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wizardProperty"]/div/div[1]/button[1]')))
    botton3.click()
    # Step4 finish
    botton4 = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]/div/div[1]/button[2]')))
    botton4.click()
    # step 5 download
    botton5 = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[3]/div[1]/div/button')))
    botton5.click()
    time.sleep(2)
    os.system("mv ~/Downloads/lipea_results.xls .")
    print("LIPEA DONE")
    browser.close()
