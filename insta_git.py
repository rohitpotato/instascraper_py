from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
from bs4 import BeautifulSoup
import os
import requests
import shutil

class App:
	def __init__(self, username = 'xxxxx', password = 'xxxxx', target_username = 'xxxxx', path = 'YOUR_PATH'):
		self.username = username
		self.password = password
		self.target_username = target_username
		self.path = path
		self.error = False
		self.driver = webdriver.Chrome('chromedriver.exe')
		self.main_url = 'https://instagram.com'
		self.driver.get(self.main_url)
		sleep(3)
		self.log_in()
		sleep(1)
		if self.error is False:
			self.open_targetProfile()
		if self.error is False:
			self.scroll_down()
		if self.error is False:
			if not os.path.exists(path):
				os.mkdir(path)
			self.download_images()
		input('Stop for now')
		sleep(3)
		self.driver.close()

	def scroll_down(self):
		try:

			no_of_posts = self.driver.find_element_by_xpath('//span[@class="g47SY "]')
			no_of_posts = str(no_of_posts.text).replace(',', '')
			self.no_of_posts = int(no_of_posts)
			if self.no_of_posts > 12:
				no_of_scrolls = int(self.no_of_posts/12) + 3
				try:

					for value in range(no_of_scrolls):
						self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
						sleep(2)

				except Exception as e:
					self.error = True
					print e
					print 'Unable to scroll down'

			sleep(10)
		except Exception:	
			print 'Unable to find the no of posts while trying to scroll down'
			self.error = True

	def open_targetProfile(self):
		try:

			search_bar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
			search_bar.send_keys(self.target_username)
			target_profileUrl = self.main_url + '/' + self.target_username + '/'
			self.driver.get(target_profileUrl)
			sleep(3)
		except Exception:
			print "Unable to find the search bar"
			self.error = True

	def log_in(self, ):
		try:
			log_in_button = self.driver.find_element_by_xpath('//p[@class="izU2O"]/a')
			log_in_button.click()
			sleep(3)
			try:

				username_input = self.driver.find_element_by_xpath('//input[@name="username"]')
				username_input.send_keys(self.username)
				password_input = self.driver.find_element_by_xpath('//input[@name="password"]')
				password_input.send_keys(self.password)
				password_input.submit()
			except Exception:
				print 'Some exception occured trying to find username or password field'
				self.error = True

		except Exception:
			self.error = True
			print 'Unable to find log in button'


	def download_images(self):
		soup = BeautifulSoup(self.driver.page_source, 'lxml')
		all_images = soup.find_all('img')
		caption_folderPath = os.path.join(self.path, 'captions')
		print 'Downloading Captions....Please Wait....'
		self.downloadCaptions(all_images, caption_folderPath)
		print len(all_images)
		for index, image in enumerate(all_images):
			filename = 'image_' + str(index) + '.jpg'
			image_path = os.path.join(self.path, filename)
			link = image['src']
			print 'Downloading images' + str(index)
			response = requests.get(link, stream = True)
			try:

				with open(image_path, 'wb') as file:
					shutil.copyfileobj(response.raw, file)
			except Exception as e:
				print 'Could not download image' + str(index)
				print 'Image link -------->' + link
				print e

	def downloadCaptions(self, images, captionPath):
		workbook = Workbook(captionPath + 'captions.xlsx')
		worksheet = workbook.add_worksheet()
		row = 0
		worksheet.write(row, 0, 'Image name')
		worksheet.write(row, 1, 'Caption')
		filename = 'captions.csv'

		row += 1
		for index, image in enumerate(images):
			filename = 'image_' + str(index) + '.jpg'
			try:
				caption = image['alt']
			except keyError:
				caption = 'No caption exists'
			worksheet.write(row, 0, filename)
			worksheet.write(row, 1, caption)
			row += 1
		workbook.close()

if __name__ == '__main__':
	app = App()
