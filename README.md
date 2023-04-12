# [Patched] PSARipper

> This script is currently PATCHED by psa.re. Their /exit/ gateway now directly has the shortner link instead of the base64 url. Will remove this notice once I figure out a way to bypass this hurdle and update the code. For now however, this script has been patched. My thinking is that they are probably dynamically generating their /exit/ gateway page serverside by doing a lookup on their database and randomizing and returning a shortner link. Pretty nifty way to stop this script, gotta admit. Also I see the "canttouchthis" at the end of the decoded base64 in the exit url :P. Good job, PSA team. :)

Shortner Bypass for PSARips (psa.re) and associated mirrors

CLI tool to bypass the PSA shortner links and return the final list of all the hosters hosting the episodes

## Pre-Requisites:

- This script requires Python 3.6+ to run
- To run the script first install all dependencies using the following command
```bash
$ pip install -r requirements.txt
```

## Usage:

```bash
$ python PSA.py <OPTIONAL: url> <OPTIONAL: mode>
```
- url: the PSA url that you want to rip. If unspecified, the script will ask you for a URL.
- mode: can either be `latest`, `full`, `1080p`, `720p`. Latest will bypass shortners of just the latest episode (incase of a TV show). Full will bypass the shortners of every episode. This setting does not matter for movies. If nothing is specified, the script will ask you for a mode.
- The output will be stored as a `.log` file (can be viewed by any text editor) in the `output` folder

## RSS Feed:

You can generate an RSS feed of the bypassed URLs by running the following command
```bash
$ python PSA.py --rss
```
The rss feed will be saved as `rss.xml` in the `output` folder

## Contributing:

All contributions to the code are welcome

## Purpose:

The purpose for this project is purely for educational purposes. PSARips is one of the few sites who have made an effort to strengthen their shortners to prevent bypasses. This to me makes it more worthwhile and fun to find ways to find vulnerabilities in their setup. I have had PSA broken for a couple of months now and I have had to change my code 3 times to account for the changes they made with how they serve their URLs. I hope that with this repo being public, they will patch out the vulnerabilities that make this code possible so I can have more fun breaking whatever patch they come up with in the future :) Because it's just too easy right now, best to make the game fair!

For documentation purposes, the following have been their changelog of my code so far

> First bypass: Location being passed as base64 encoded url in header

> Patched First bypass; New vulnerability: Location being passed as a redirect url after ?url= paramater after the shortner link 

> Patched Second bypass; Forgot to patch back the first issue, so first bypass code started working again

> Patched Third bypass; New vulnerability: Response bytes of the /exit/ url once decoded via utf8 returns a base64 of the final location

> 4/7/2020; 5:20 PM SGT: Patched public script; Added revalidation with a redirect if no cache was present. Easy enough to break, just call via cfscrape again, this time the session has a cache and should be able to view the underlying url just fine without any unnecessary 302s

> 5/7/2020; 3:00 PM SGT: Patched script

The script so far has been patched unsuccessfully `4` times. 
