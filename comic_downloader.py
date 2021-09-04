from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import bs4, os, sys, urllib.request, time, progressbar

custom_path = str(input("Want to save to a custom path? "))
if custom_path == "y" or custom_path == "Y":
    parentdir = input("Please enter the path you want to save to ")
else:
    parentdir = 'C:/Users/starr/Documents/Comics'
dir = input("What is the comic name? ")
path = os.path.join(parentdir, dir)
os.mkdir(path)
print("Directory %s created" % path)

every_issue = input("Press 1 to download just one issue, 2 to download the entire series, 3 to download the series starting from a certain spot ")

if len(sys.argv) > 1:
    url = sys.argv[1]
    print(url)
else:
    url = input("Enter a comic link pls: ")
    print(url)

if every_issue == "1":
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options = options, executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
    url = url+"/Issue-1"
    res = driver.get(url)
    print('Downloading page %s...' % url)
    soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
    subject_options = soup.findAll('select', attrs = {'id': 'selectPage'} )[0].findAll("option")
    for i in range(len(subject_options)):
        comicElem = driver.find_element_by_css_selector("#imgCurrent")
        comicUrl = comicElem.get_attribute("src")
        print('Downloading image %s...' % (comicUrl))
        urllib.request.urlretrieve(comicUrl, path+"/" + str(i+1) + ".png")
        print('Downloading page %s...' % (url+"#"+str(i+2)))
        newurl = url+"#"+str(i+2)
        print(newurl)
        driver.close()
        driver = webdriver.Firefox(options = options, executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
        res = driver.get(newurl)
    driver.close()
if every_issue == "2":
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options = options, executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
    new_url = url+"/Issue-1"
    print('Downloading page %s...' % new_url)
    os.mkdir(path+"/1")
    res = driver.get(new_url)
    soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
    num_issues = soup.findAll('select', attrs = {'id': 'selectEpisode'} )[0].findAll("option")
    for i in progressbar.progressbar(range(len(num_issues))):
        num_pages = soup.findAll('select', attrs = {'id': 'selectPage'} )[0].findAll("option")
        for j in progressbar.progressbar(range(len(num_pages))):
            comicElem = driver.find_element_by_css_selector("#imgCurrent")
            comicUrl = comicElem.get_attribute("src")
            print('Downloading image %s...' % (comicUrl))
            urllib.request.urlretrieve(comicUrl, path+ "/" + str(i+1) + "/" + str(j+1) + ".png")
            print('Downloading page %s...' % (url+"#"+str(j+2)))
            newurl = new_url+"#"+str(j+2)
            print(newurl)
            driver.close()
            driver = webdriver.Firefox(options = options, executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
            res = driver.get(newurl)
        driver.close()
        new_url = url+"/Issue-" + str(i+2)
        os.mkdir(path+"/"+str(i+2))
        res = driver.get(new_url)
        soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
    driver.close()

if every_issue == "3":
    #options = Options()
    #options.headless = True
    driver = webdriver.Firefox(executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
    issue = input("What issue? ")
    page = input("What page? ")
    new_url = url+"/Issue-%s#%s" %(issue, page)
    print('Downloading page %s...' % new_url)
    os.mkdir(path+"/%s" % issue)
    res = driver.get(new_url)
    print(res)
    soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
    #print (soup.prettify())
    num_issues = soup.findAll('select', attrs = {'id': 'selectEpisode'} )[0].findAll("option")
    print("num issues is %s" %len(num_issues))
    for i in progressbar.progressbar(range(int(issue), len(num_issues))):
        num_pages = soup.findAll('select', attrs = {'id': 'selectPage'} )[0].findAll("option")
        j = 0
        for j in progressbar.progressbar(range(int(page), len(num_pages)+1)):
            print(j)
            #if j == len(num_pages+1):
            #    break
            comicElem = driver.find_element_by_css_selector("#imgCurrent")
            comicUrl = comicElem.get_attribute("src")
            print('Downloading image %s...' % (comicUrl))
            print(path)
            urllib.request.urlretrieve(comicUrl, path+ "/" + str(i) + "/" + str(j) + ".png")
            print('Downloading page %s...' % (url+"/Issue-%s#%s" %(str(i), str(j+1))))
            newurl = url+"/Issue-%s#%s" %(str(i), str(j+1))
            print(newurl)
            driver.close()
            driver = webdriver.Firefox(executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
            res = driver.get(newurl)
            # if j+1 == len(num_pages):
            #     comicElem = driver.find_element_by_css_selector("#imgCurrent")
            #     comicUrl = comicElem.get_attribute("src")
            #     print('Downloading image %s...' % (comicUrl))
            #     print(path)
            #     urllib.request.urlretrieve(comicUrl, path+ "/" + str(i) + "/" + str(j) + ".png")
        #driver.close()
        new_url = url+"/Issue-" + str(i+1)
        print(new_url)
        os.mkdir(path+"/"+str(i+1))
        res = driver.get(new_url)
        soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
        num_pages = soup.findAll('select', attrs = {'id': 'selectPage'} )[0].findAll("option")
        print("num pages is %s" %len(num_pages))
        page = 1
    driver.close()