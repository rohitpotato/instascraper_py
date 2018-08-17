from selenium import webdriver
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
from time import sleep
import os
import requests
import shutil
import getpass
import csv

def login(username, password, driver):
	loginButton = driver.find_element_by_xpath('//p[@class="izU2O"]/a')
	loginButton.click()
	sleep(3)
	try:
		userInput = driver.find_element_by_xpath('//input[@name="username"]')
		userInput.send_keys(username)
		passwordInput = driver.find_element_by_xpath('//input[@name="password"]')
		passwordInput.send_keys(password)
		passwordInput.submit()
		sleep(3)
	except Exception:
		print "Could not find username or passwor input fields"

def openTargetProfile(driver, target_profile):
	mainUrl = 'https://www.instagram.com'
	try:

		search_bar = driver.find_element_by_xpath('//input[@placeholder="Search"]')
		search_bar.send_keys(target_profile)
		target_profile_url = mainUrl + '/' + target_profile + '/'
		driver.get(target_profile_url)
		sleep(1)

	except Exception:
		print "Unable to open target_profile"


def scrollDown(driver):
	try:
		noOfPosts = driver.find_element_by_xpath('//span[@class="g47SY "]')
		noOfPosts = int(str(noOfPosts.text).replace(',', ''))
		if noOfPosts > 12:
			noOfScrolls = (noOfPosts/12) + 3
			try:

				for value in range(noOfScrolls):
					driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
					sleep(2)
			except Exception:
				print "Unable to Scroll Down"

		sleep(10)	

	except Exception as e:
		print "Unable to find the no of posts"
		print e

def findAndDownloadImages(driver, path):
	if not os.path.exists(path):
		os.mkdir(path)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	all_images = soup.find_all('img')
	print "Downloading captions...Please wait..."
	downloadCaptionsToExcel(driver, all_images, path)
	print len(all_images)
	for index, image in enumerate(all_images):
		image_name = 'Image_' + str(index) + '.jpg'
		image_path = os.path.join(path, image_name)
		print "Downloading Images" + str(index)
		image_file = requests.get(image['src'], stream = True)
		try:
			with open(image_path, 'wb') as file:
				shutil.copyfileobj(image_file.raw, file)
		except Exception as e:
			print "Error downloading Image -------->" + str(index) 
			print "Image Url------->" + image[src]
			print e

def downloadCaptionsToExcel(driver, all_images, path):
	workbook = Workbook(path + 'captions.xlsx')
	worksheet = workbook.add_worksheet()
	row = 0
	worksheet.write(row, 0, 'Image name')
	worksheet.write(row, 1, 'Caption')
	filename = 'captions.csv'

	row += 1
	for index, image in enumerate(all_images):
		filename = 'image_' + str(index) + '.jpg'
		try:
			caption = image['alt']
		except Exception:
			caption = 'No caption exists'
		worksheet.write(row, 0, filename)
		worksheet.write(row, 1, caption)
		row += 1
	workbook.close()



def scrapeImages(username, password, target_profile, path):
	driver = webdriver.Chrome('chromedriver.exe')
	driver.get('https://www.instagram.com')
	sleep(3)
	login(username, password, driver)
	sleep(3)
	openTargetProfile(driver, target_profile)
	sleep(2)
	scrollDown(driver)
	sleep(1)
	findAndDownloadImages(driver, path)
	sleep(2)
	driver.close()


username = raw_input('Enter your username:')
password = getpass.getpass("Enter your password, do not worry... it's invisible:")
target_profile = raw_input('Enter the target Profile:')
path = 'C://users/rohit/desktop/instapics'
target_path = os.path.join(path, target_profile)

scrapeImages(username, password, target_profile, target_path)

