import requests
import configparser
import click
import json
import sys
from os.path import exists
from pathlib import Path

Config = configparser.ConfigParser()


def phishtank(phishurl):
    global phishtank_enabled
    service = 'PhishTank'

    if phishtank_enabled:

        s = requests.Session()

        if dry_run:
            dryrun_report(phishurl, service)
            return

        login = s.post('https://phishtank.org/login.php', data={
                       'username': phishtank_username, 'password': phishtank_password, 'Login': 'Sign+In'})

        if login.text.find('Your sign in attempt was unsuccessful') != -1:
            click.echo(
                'Failed to sign into PhishTank. The PhishTank module has been disabled for this run.', err=True)
            phishtank_enabled = False

        report = s.post('https://phishtank.org/add_web_phish.php', data={
                        'phish_url': phishurl, 'phish_target': '8', 'phish_text': 'null', 'phish_submit': 'Submit'})

        if report.text.find('Thank you for your submission. It has been added to the queue for processing and the status will be updated on your dashboard shortly.') != -1:
            click.echo(f'URL {phishurl} successfully reported to PhishTank.')

        elif report.text.find('That URL has already been submitted') != -1:
            click.echo(f'URL {phishurl} already reported to PhishTank.')
        else:
            click.echo(
                'Unknown error occured while submitting URL to PhishTank.', err=True)

    else:
        return


def netcraft(phishurl):
    service = 'Netcraft'

    if netcraft_enabled:

        headers = {'Content-Type': 'application/json'}
        data = {"urls": [{"url": phishurl}], "email": netcraft_email}

        if dry_run:
            dryrun_report(phishurl, service)
            return

        report = requests.post(
            'https://report.netcraft.com/api/v3/report/urls', headers=headers, data=json.dumps(data))

        if report.status_code == 200:
            click.echo(f'URL {phishurl} successfully reported to Netcraft.')
        elif report.text.find('Duplicate of a recent submission') != -1:
            click.echo(f'URL {phishurl} already reported to Netcraft.')
        elif report.status_code == 429:
            click.echo('Netcraft is rate limiting your submissions.', err=True)
        else:
            click.echo(
                'An error occured while submitting URL to Netcraft.', err=True)

    else:
        return


def urlscan(phishurl):
    service = 'urlscan.io'

    if urlscan_enabled:

        headers = {'API-Key': urlscan_api_key,
                   'Content-Type': 'application/json'}
        data = {"url": phishurl, "visibility": urlscan_scan_visibility}

        if dry_run:
            dryrun_report(phishurl, service)
            return

        report = requests.post(
            'https://urlscan.io/api/v1/scan/', headers=headers, data=json.dumps(data))
        if report.status_code == 200:
            click.echo(f'URL {phishurl} successfully submitted to urlscan.io')
        elif report.status_code == 429:
            click.echo(
                'urlscan.io is rate limiting your submissions.', err=True)
        else:
            click.echo(
                'An error occured while submitting URL to urlscan.io.', err=True)

    else:
        return


def setconfigs(config):
    global phishtank_enabled
    global netcraft_enabled
    global urlscan_enabled
    global phishtank_username
    global phishtank_password
    global netcraft_email
    global urlscan_api_key
    global urlscan_scan_visibility

    if config == None:
        if exists('config.ini') == False:
            click.echo(
                'No config specified, and config.ini could not be found. Exiting.', err=True)
            sys.exit()
        config = 'config.ini'  # Fall back to config.ini in current dir if none is specified

    if exists(config):
        configfile = Path(config)
        try:
            Config.read(configfile)
        except configparser.MissingSectionHeaderError:
            click.echo(f'Could not parse config file {config}', err=True)
            sys.exit()
    else:
        click.echo(f'Could not open config file {config}', err=True)
        sys.exit()

    try:
        phishtank_enabled = Config.getboolean('phishtank', 'enabled')
    except configparser.NoSectionError:
        pass
    try:
        netcraft_enabled = Config.getboolean('netcraft', 'enabled')
    except configparser.NoSectionError:
        pass
    try:
        urlscan_enabled = Config.getboolean('urlscan', 'enabled')
    except configparser.NoSectionError:
        pass

    try:
        phishtank_username = Config.get('phishtank', 'username')
        phishtank_password = Config.get('phishtank', 'password')
    except configparser.NoSectionError:
        phishtank_enabled = False
    try:
        netcraft_email = Config.get('netcraft', 'email')
    except configparser.NoSectionError:
        netcraft_enabled = False
    try:
        urlscan_api_key = Config.get('urlscan', 'api_key')
        urlscan_scan_visibility = Config.get('urlscan', 'scan_visibility')
    except configparser.NoSectionError:
        urlscan_enabled = False


def modulecheck():
    if (phishtank_enabled == netcraft_enabled == urlscan_enabled == False):
        click.echo(
            'All modules disabled. Please check your config file', err=True)
        sys.exit()


def dryrun_report(phishurl, service):  # handle dry-runs by doing nothing
    click.echo(
        f'{service} module did nothing to {phishurl} as this is a dry run.')


@click.option('--config', help='Path of config.ini. Will look in the current directory if not specified.', type=str)
# @click.option('--generate-config', is_flag=True, callback=generate_config, expose_value=False, is_eager=True)
@click.option("--url", help='Report a single URL.', type=str)
@click.option("--file", help='Report a list of URLs, separated by newlines.', type=str)
@click.option('--dry-run', 'dryrun', help='Do not actually submit URLs to services.', flag_value=True)
@click.command(no_args_is_help=True)
def reporting(file, config, url, dryrun):
    """Tool to report phishing URLs to security services.

    Set API keys in config.ini

    Currently supports PhishTank, Netcraft, and urlscan.io."""
    global dry_run
    dry_run = dryrun

    setconfigs(config)

    if url is not None:
        modulecheck()
        url = "".join(url.split())  # remove whitespace
        phishtank(url)
        netcraft(url)
        urlscan(url)

    if file is not None:

        try:
            with click.open_file(file) as phishlist:
                for phish in phishlist:
                    modulecheck()
                    phish = "".join(phish.split())
                    phishtank(phish)
                    netcraft(phish)
                    urlscan(phish)
        except FileNotFoundError:
            click.echo(f'Could not read {file}', err=True)
            exit()

    else:
        click.echo('No URLs to process.')


if __name__ == '__main__':
    reporting()
