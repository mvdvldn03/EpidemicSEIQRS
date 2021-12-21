import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=____")
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

def get_cases():
    x = driver.find_elements_by_xpath("//div[@class='_26ZypQtR8sLPiXEB1jzI1b']/*[name()='svg']")[2]
    x = x.find_elements_by_xpath("./*[name()='g']")[5].get_attribute("outerHTML")
    d = x[x.index("d=")+2:x.index(" fill")].split(',')[2:-1]
    for i in range(len(d)):
        d[i] = d[i].split('L')[0]

    mov_len = 14
    bounds = driver.find_elements_by_xpath("//div[@class='_26ZypQtR8sLPiXEB1jzI1b']/*[name()='svg']/*[name()='g']")[22].text
    bounds = bounds.split('\n')[-1]

    if 'M' in bounds:
        bounds = int(bounds.replace('M', '000000').replace(".",""))
    elif 'k' in bounds:
        bounds = int(bounds.replace('k','000').replace(".",""))
    else:
        bounds = int(bounds.replace(".",""))

    d = [(335 - float(x))*(bounds/335) for x in d]
    d = [sum(d[i-(mov_len-1):i+1]) if i>(mov_len-1) else sum(d[:i+1]) for i in range(len(d))][24:247]
    return d

def get_mask():
    x = driver.find_elements_by_xpath("//div[@class='_26ZypQtR8sLPiXEB1jzI1b']")[4]
    x = x.find_elements_by_xpath("./*[name()='svg']/*[name()='g']")[6]
    x = x.find_elements_by_xpath("./*[name()='path']")[2].get_attribute("outerHTML")
    d = x[x.index("d=") + 2:x.index(' stroke=')].split(',')[2:-1]

    for i in range(len(d)):
        d[i] = float(d[i].split('L')[0])

    d = [round(100 - (x/335)*100,4) for x in d][17:240]
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

    d = [round(top - (x / 235) * (top - bottom), 4) for x in d][17:240]
    return d

def get_rt():
    x = driver.find_elements_by_xpath("//div[@class='RTSubareaOverview__RTChartWrapper-sc-1idngnz-8 egOaQg']/*[name()='svg']/*[name()='g']/*[name()='g']/*[name()='g']")[-2].get_attribute("outerHTML")
    d = x[x.index("d=") + 2:x.index(' stroke-dasharray=')].split(',')[2:-1]

    for i in range(len(d)):
        d[i] = float(d[i].split('L')[0])

    height = driver.find_element_by_xpath("//div[@class='RTSubareaOverview__RTChartWrapper-sc-1idngnz-8 egOaQg']/*[name()='svg']").get_attribute("outerHTML")
    height = float(height[height.index("height=") + 8:height.index(" class") - 1])

    x = driver.find_elements_by_xpath("//div[@class='RTSubareaOverview__RTChartWrapper-sc-1idngnz-8 egOaQg']/*[name()='svg']/*[name()='g']/*[name()='g']/*[name()='g']")[2]
    x = x.find_elements_by_xpath("./*[name()='g']")
    t1 = x[0].get_attribute("outerHTML")
    t1 = [float(x[0].text), float(t1[t1.index("translate(0,")+12:t1.index(')')])]

    t2 = x[1].get_attribute("outerHTML")
    t2 = [float(x[1].text), float(t2[t2.index("translate(0,") + 12:t2.index(')')])]

    A = np.array([[t1[1], height-t1[1]], [t2[1], height-t2[1]]])
    B = np.array([height*t1[0],height*t2[0]])
    val = np.linalg.solve(A, B)

    d = [round((val[1] - (x/height)*(val[1] - val[0])),4) for x in d][3:226]
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

if __name__ == "__main__":
    state_names = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    state_codes = [ 'AL', 'AK','AZ', 'AR', 'CA', 'CO', 'CT', 'DE','FL', 'GA','HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    for i in range(len(state_codes)):
        n = state_names[i]
        n = n.replace(" ", "-").lower()

        c = state_codes[i]

        driver.get(f"http://covid19.healthdata.org/united-states-of-america/{n}?view=infections-testing&tab=trend&test=infections")
        time.sleep(10)
        case_arr = get_cases()
        mask_arr = get_mask()
        movement_arr = get_movement()

        driver.get(f"https://www.google.com/search?q={n}-state-population")
        time.sleep(10)
        pop = get_pop()

        print(f"{n.replace('-', '_')}_frac = {[round(x/pop,4) for x in case_arr]};")
        print(f"{n.replace('-', '_')}_mask = {mask_arr};")
        print(f"{n.replace('-', '_')}_movement = {movement_arr};")

        driver.get(f"https://rt.live/us/{c}")
        time.sleep(10)
        rt = get_rt()
        print(f"{c}_rt = {rt};")

    driver.quit()
