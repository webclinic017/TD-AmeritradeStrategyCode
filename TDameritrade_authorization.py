import time
import urllib
import requests
from splinter import Browser  
from config import client_id,password,accntNmber,userName
import os

class TDAuthentication(object):

    def __init__(self,client_id,accntNmber,password):
        self.client_id = client_id
        self.accntNmber = accntNmber
        self.password = password
        self.access_code = None
        self.access_token = None

    def _get_access_code(self):

        # define a location of the chrome driver
        executable_path = {'executable_path': r'C:\Users\dmac0\chromedriver'}

        # create new instance of chrome
        browser = Browser('chrome', **executable_path, headless = False)

        #define the components of the url
        method = 'GET'
        url = 'https://auth.tdameritrade.com/auth?'
        client_code = client_id + '@AMER.OAUTHAP'
        payload = {'response_type':'code','redirect_uri':'http://localhost/', 'client_id':client_code}

        #Build URL
        built_url = requests.Request(method, url, params = payload).prepare()
        built_url = built_url.url

        #go to URL
        browser.visit(built_url)

        # define elements to pass through to the form
        payload_login = {'username':userName, 'password':password}

        # Fill out each element in the form
        browser.find_by_id('username').first.fill(payload_login['username'])
        browser.find_by_id('password').first.fill(payload_login['password'])
        browser.find_by_id('accept').first.click()
        time.sleep(2)

        # Get the Text Message Box
        browser.find_by_text('Can\'t get the text message?').first.click()
        time.sleep(2)

        # Get the Answer Box
        browser.find_by_value("Answer a security question").first.click()
        time.sleep(2)

        # Answer the Security Questions.
        if browser.is_text_present('What is your paternal grandfather\'s first name?'):
	        browser.find_by_id('secretquestion').first.fill('William')

        elif browser.is_text_present('In what city was your high school?'):
	        browser.find_by_id('secretquestion').first.fill('camillus')

        elif browser.is_text_present('What was the name of your first pet?'):
	        browser.find_by_id('secretquestion').first.fill('buddy')

        elif browser.is_text_present('What is your father\'s middle name?'):
	        browser.find_by_id('secretquestion').first.fill('william')

        elif browser.is_text_present('What was your high school mascot?'):
	        browser.find_by_id('secretquestion').first.fill('wildcat')

        browser.find_by_id('accept').first.click()

        time.sleep(3)
        # click to accept terms and conditions
        browser.find_by_id('accept').first.click()

        # Give it time to load
        time.sleep(2)
        new_url = browser.url

        # grab url and parse
        parse_url = urllib.parse.unquote(new_url.split('code=')[1])

        #close the browser
        browser.quit()

        #print(parse_url)

        #define endpoinpoint
        url = r'https://api.tdameritrade.com/v1/oauth2/token'

        #define the header
        headers = {'Content-Type':'application/x-www-form-urlencoded'}

        #define payload
        payload_oath = {'grant_type':'authorization_code',
                        'access_type':'offline',
                        'code':parse_url,
                        'client_id':client_id,
                        'redirect_uri':'http://localhost/'}

        #post the data to get the token
        authReply = requests.post(url, headers = headers, data = payload_oath)

        #convert to json
        decoded_content = authReply.json()
        #print(decoded_content)

        access_token = decoded_content['access_token']

        os.environ['td_token'] = str(access_token)
        self.access_token = access_token

    def authenticate(self):
        try:
            self.access_token = os.environ['td_token']
        except KeyError:
            self._get_access_code()