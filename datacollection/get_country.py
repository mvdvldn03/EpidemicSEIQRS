#March 10 to Week Before Date Collected

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import sys, traceback

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=____")
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

#IHME - starts collecting data on February 4 (35 days)
def get_cases():
    x = driver.find_elements_by_xpath("//div[@class='_26ZypQtR8sLPiXEB1jzI1b']/*[name()='svg']")[3]
    x1 = x.find_elements_by_xpath("./*[name()='g']")[5].get_attribute("outerHTML")
    d = x1[x1.index("d=") + 2:x1.index(" fill")].split(',')[2:-1]
    for i in range(len(d)):
        d[i] = d[i].split('L')[0]

    mov_len = 14
    x2 = x.find_elements_by_xpath("./*[name()='g']")[0]
    b1 = str2int(x2.find_elements_by_xpath("./*[name()='g']")[0].text)
    b2 = str2int(x2.find_elements_by_xpath("./*[name()='g']")[-1].text)

    d = [round((335 - float(x)) * ((b2 - b1) / 335) + b1, 4) for x in d]
    d = [sum(d[i - (mov_len - 1):i + 1]) if i > (mov_len - 1) else sum(d[:i + 1]) for i in range(len(d))][
        35:(date.today() - date(2020, 3, 10)).days + 28]
    return d

#IHME - starts collecting mask/movement data on February 8 (31 days)
def get_mask():
    x = driver.find_elements_by_xpath("//div[@class='_26ZypQtR8sLPiXEB1jzI1b']")[4]
    x = x.find_elements_by_xpath("./*[name()='svg']/*[name()='g']")[6]
    x = x.find_elements_by_xpath("./*[name()='path']")[2].get_attribute("outerHTML")
    d = x[x.index("d=") + 2:x.index(' stroke=')].split(',')[2:-1]

    for i in range(len(d)):
        d[i] = float(d[i].split('L')[0])

    d = [round(100 - (x/335)*100,4) for x in d][31:(date.today()-date(2020,3,10)).days+24]
    return d

def get_movement():
    x = driver.find_elements_by_xpath("//div[@class='_330a1JhpT32TjXb-mMlqri']/*[name()='svg']/*[name()='g']")[5]
    x = x.find_elements_by_xpath("./*[name()='path']")[3].get_attribute("outerHTML")

    d = x[x.index("d=") + 2:x.index(' fill=')].split(',')[2:-1]

    for i in range(len(d)):
        d[i] = float(d[i].split('L')[0])

    y = driver.find_elements_by_xpath("//div[@class='_330a1JhpT32TjXb-mMlqri']/*[name()='svg']/*[name()='g']")[0]
    y = y.find_elements_by_xpath("./*[name()='g']")
    top = float(y[-1].text[:-1])
    bottom = float(y[0].text[:-1])

    d = [round(top - (x / 235) * (top - bottom), 4) for x in d][31:(date.today()-date(2020,3,10)).days+24]
    return d

def get_pop():
    try:
        pop = driver.find_element_by_xpath("//div[@class='ayqGOc kno-fb-ctx KBXm4e']").text[:-7]
    except:
        pop = driver.find_element_by_xpath("//div[@class='ayqGOc kno-fb-ctx kpd-lv kpd-le KBXm4e']").text[:-7]

    pop = pop.replace(",", "")
    if "million" in pop:
        pop = float(pop.split()[0]) * 1000000
    else:
        pop = int(pop)
    return pop

def get_vaccination():


def str2int(string):
    if 'M' in string:
        return int(float(string[:-1])*1000000)
    elif 'k' in string:
        return int(float(string[:-1])*1000)
    else:
        return int(string)

if __name__ == "__main__":
    try:
        country_name = sys.argv[1].lower()

        driver.get(f"http://covid19.healthdata.org/{country_name}?view=infections-testing&tab=trend&test=infections")
        time.sleep(15)
        case_arr = get_cases()
        mask_arr = get_mask()
        movement_arr = get_movement()

        driver.get(f"https://www.google.com/search?q={country_name.replace('-',' ')} state population")
        time.sleep(15)
        pop = get_pop()

        minimum_case = round(case_arr[next((i for i, x in enumerate(case_arr) if x), None)]/pop,10)
        print(f"{pop};{[round(x/pop,10) if x > 0 else minimum_case for x in case_arr]};{mask_arr};{movement_arr}")
    except:
        driver.save_screenshot(f"{country_name}.png")
        print(traceback.format_exc())
    finally:
        driver.quit()
