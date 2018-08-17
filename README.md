<h1>InstagramPy</h1>

<p>Instagram Image and Caption Downlaoder. </p>

<h2>Getting Started</h2>

Clone the project by running: ``` git clone https://github.com/rohitpotato/instascraper_py.git ``` 

<h2>Prerequisites</h2>

<p>You must have Python 2.7+ or equivalent installed on your machine. </p2>

<p>Python 3 users might have to change some things around. </h2>

<b>For example: </b>

``` Change print "something" to print("something") ```

``` Change username = raw_input() to -----> username = input() ```

<h2>Running this projcet</h2>

<p>Navigate to the directory where you cloned the project. </p>

<p>There are 2 versions of this application both included in this repo. </p>

First version involves hardcoding your credentials in the main file.

The second version allows you to specify your credentials at the command line, making it dynamic. </p>

<h3> For the first version: </h3>

You need to add your credentials in the class constructor.

<b>Example</b>
```
class App:
	def __init__(self, username = 'obiwan', password = 'hellothere', target_username = 'skywalker', path = 'users/rohit/desktop/instapics'):
 
 ```
 <h2>Libraries Used</h2>
 ```
 BeautifulSoup
 Selenium
 Chrome Webdriver
 Requests
 ```
 Setting these up is fairly straight forward using pip.
 
 <h2>Note</h2>
 <b>Since Instagram changes around its structure, the application might stop working.
 For Handling that, try except blocks have been used to identify the cause of error. </b>
 
 <h2>Happy Scraping </h2>
