import requests
import configparser
import click
import json
import sys
from os.path import exists

Config = configparser.ConfigParser()

def phishtank(phishurl):

    s = requests.Session()

    login = s.post('https://phishtank.org/login.php', data={'username': phishtank_username, 'password': phishtank_password, 'Login': 'Sign+In'})

    if login.text.find('Your sign in attempt was unsuccessful') != -1:
        print('Failed to sign into PhishTank. Aborting.')
        exit(1)

    report = s.post('https://phishtank.org/add_web_phish.php', data={'phish_url': phishurl, 'phish_target': '8', 'phish_text': 'null', 'phish_submit': 'Submit'})

    if report.text.find('Thank you for your submission. It has been added to the queue for processing and the status will be updated on your dashboard shortly.') != -1:
        print('URL', phishurl, 'successfully reported to PhishTank.')
        
    elif report.text.find('That URL has already been submitted') != -1:
        print('URL', phishurl, 'already reported to PhishTank.')

    else:
        print('Unknown error occured while submitting URL to PhishTank.')


def netcraft(phishurl):

	headers = {'Content-Type':'application/json'}
	data = {"urls": [{ "url": phishurl}], "email": netcraft_email}
	report = requests.post('https://report.netcraft.com/api/v3/report/urls',headers=headers, data=json.dumps(data))

	if report.status_code == 200:
		print('URL', phishurl, 'successfully reported to Netcraft.')
	elif report.text.find('Duplicate of a recent submission') != -1:
		print('URL', phishurl, 'already reported to Netcraft.')
	elif report.status_code == 429:
		print('Netcraft is rate limiting your submissions.')
	else:
		print('An error occured while submitting URL to Netcraft.')

def urlscan(phishurl):
	headers = {'API-Key':urlscan_api_key,'Content-Type':'application/json'}
	data = {"url": phishurl, "visibility": urlscan_scan_visibility}
	report = requests.post('https://urlscan.io/api/v1/scan/',headers=headers, data=json.dumps(data))
	if report.status_code == 200:
		print('URL', phishurl, 'successfully submitted to urlscan.io.')
	elif report.status_code == 429:
		print('urlscan.io is rate limiting your submissions.')
	else:
		print('An error occured while submitting URL to urlscan.io.')

def setconfigs(config):
	if config is None:
		if exists('config.ini') is False:
			print('No config specified, and config.ini could not be found. Exiting.')
			sys.exit()
		config = 'config.ini' # Fall back to config.ini in current dir if none is specified
	
	global phishtank_username
	global phishtank_password
	global netcraft_email
	global urlscan_api_key
	global urlscan_scan_visibility
	
	try:
		Config.read(config)
		phishtank_username = Config.get('phishtank', 'username')
		phishtank_password = Config.get('phishtank', 'password')
		netcraft_email     = Config.get('netcraft', 'email')
		urlscan_api_key     = Config.get('urlscan', 'api_key')
		urlscan_scan_visibility     = Config.get('urlscan', 'scan_visibility')
	except configparser.NoSectionError:
		print('Could not read the config file or options are missing.')
		exit()

@click.option('--config', help='path of config.ini.', type=str)
#@click.option('--generate-config', is_flag=True, callback=generate_config, expose_value=False, is_eager=True)
@click.option("--url", help='report a single URL.', type=str)
@click.option("--file", help='report a list of URLs, separated by newlines.', type=str)
@click.command(no_args_is_help=True)
def reporting(file,config,url):
	
	"""Tool to report phishing URLs to security companies.
	
	Set API keys in config.ini
	
	Currently supports PhishTank, Netcraft, and urlscan.io."""
	
	setconfigs(config)
	
	if url is not None:
		url = "".join(url.split()) # remove whitespace
		phishtank(url)
		netcraft(url)
		urlscan(url)
		sys.exit()
	
	if file is not None:
	
		try:
			with click.open_file(file) as phishlist:
				for phish in phishlist:
					phish = "".join(phish.split())
					phishtank(phish)
					netcraft(phish)
					urlscan(phish)
		except FileNotFoundError:
			print('Could not read', file)
			exit()


if __name__ == '__main__':
	reporting()
