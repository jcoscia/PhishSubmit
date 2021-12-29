# PhishSubmit
Tool to report phishing URLs to security services.

```
$ python3 phishsubmit.py
Usage: phishsubmit.py [OPTIONS]

  Tool to report phishing URLs to security services.

  Set API keys in config.ini

  Currently supports PhishTank, Netcraft, and urlscan.io.

Options:
  --dry-run      Do not actually submit URLs to services.
  --file TEXT    Report a list of URLs, separated by newlines.
  --url TEXT     Report a single URL.
  --config TEXT  Path of config.ini. Will look in the current directory if not
                 specified.

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

1. Clone the repository with `git clone https://github.com/jcoscia/PhishSubmit.git`, then enter the directory.
2. Install the dependencies. You may get these from your system's package manager, or use pip with `pip install -r requirements.txt`
3. Edit config.ini and add your credentials and API keys.

## Disclaimer
This is a tool I made for personal use, to make my workflow a bit easier. Yes, I know the code is terrible. But it *does* work. Feel free to submit pull requests or file issues.

## See also
[Abwhose](https://github.com/bradleyjkemp/abwhose)
[Phish Report](https://phish.report/)
