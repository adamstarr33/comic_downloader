from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(options = options, executable_path= r"C:\Users\starr\Documents\Dev\Web_Drivers\geckodriver.exe")
import bs4, os, sys, urllib.request

custom_path = input("Want to save to a custom path? ")
if custom_path == "y" or "Y":
    parentdir = input("Please enter the path you want to save to ")
else:
    parentdir = 'C:/Users/starr/Documents/Comics'
dir = input("What is the comic name? ")
path = os.path.join(parentdir, dir)
os.mkdir(path)
print("Directory %s created" % path)

every_issue = input("Press 1 to download just one issue or 2 to download the entire series ")

if len(sys.argv) > 1:
    url = sys.argv[1]
    print(url)
else:
    url = input("Enter a comic link pls: ")
    print(url)

if every_issue == 1:
    print('Downloading page %s...' % url)
    res = driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
    subject_options = soup.findAll('select', attrs = {'id': 'selectPage'} )[0].findAll("option")
    for i in range(len(subject_options)-1):
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
else:
    print('Downloading page %s...' % url)
    res = driver.get(url)
    soup = bs4.BeautifulSoup(driver.page_source, features="lxml")
    num_issues = soup.findAll('select', attrs = {'id': 'selectEpisode'} )[0].findAll("option")
    for i in range(len(num_issues)-1):
        os.mkdir(path+"/"+str(i+1))
        num_pages = soup.findAll('select', attrs = {'id': 'selectPage'} )[0].findAll("option")
        for i in range(len(num_pages)-1):
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

