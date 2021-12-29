# PhishSubmit
Tool to report phishing URLs to security companies.

```
$ python3 phishsubmit.py 
Usage: phishsubmit.py [OPTIONS]

  Tool to report phishing URLs to security companies.

  Set API keys in config.ini

  Currently supports PhishTank, Netcraft, and urlscan.io.

Options:
  --file TEXT    report a list of URLs, separated by newlines.
  --url TEXT     report a single URL.
  --config TEXT  path of config.ini.
  --help         Show this message and exit.
  ```

## Supported services
* [PhishTank](https://phishtank.org/)
* [Netcraft](https://report.netcraft.com/)
* [urlscan.io](https://urlscan.io/)

(will try to add more)

## Dependencies

* requests
* configparser
* click

## Installation

1. Clone the repository with `git clone https://github.com/jcoscia/PhishSubmit.git`
2. `cd PhishSubmit`
3. Install the dependencies. You may get these from your system's package manager, or use pip with `pip install -r requirements.txt`
4. Open config.ini and add your credentials and API keys.

## Disclaimer
This is a tool I made for personal use, to make my workflow a bit easier. Yes, I know the code is terrible. But it *does* work. Feel free to submit pull requests or file issues :)
