# PS4Games

First off I'd like to thank you guys for the support I've received regarding this project.

Initially I made this for myself because I wanted to see which games were newly added to a site - but then I had the idea of sharing it here to see how people reacted.

Since everyone seems to like it I have decided to release it!



# Installation
If you had the old version, delete the old GamesOutput.json

First things first you're gonna need Python, you can get it here: https://www.python.org/downloads/

Once you've got python installed open up the 'requirements.txt' file and press CTRL+A CTRL+C (copy the whole document)

Open up Command Prompt and CTRL+V (paste)

To run the program click into the folder path, type 'cmd' and then 'python app.py'

-If it's your first time running it, it will take a minute to open as it initially scrapes the games list and makes the GameOutput.json file (don't re-open the script unless it errors)

# Bugs

Please DM me with any bugs you find and I'll try my best to fix them in a timely manner.

Current bugs I know of:

-Some game links aren't always picked up by the scraper (tends to be ps2 games?)

-I know the Size calculation isn't always right, that's partially lazy programming on my part

-It's possible for the site to pseudo-rate-limit you if you make too many requests but this can be avoided by not spam-updating the games list.

-Some games CUSAs have 'p's in them that shouldn't, i would fix but hvaen't got round to it.

-Clearing the search box doesn't reset the list resulting in needing to re-open the script
# Changelog

[10/12/2023]
- Fixed problem with updating the games list
- Fixed game CUSA grabbing garbage data
  
[05/12/2023]
- Made the program run faster, added file download API
- Added support for multiple hosts
- QOL Updates

