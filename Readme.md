# Leto Theater Reactions

Allows you to queue animations for incoming donations.
The animations will wait for your idle loop to finish, so you can properly blend between them.

## Installing Python

OBS scripts need Python to run, so you will need to install it, if you haven't already.

To check if you have an installation of Python, open your Terminal and run `python --version`. If you get an error, you will have to install it.

You can find the instructions on the official [Python website](https://www.python.org/downloads/).

## Initial Setup

These steps assume that you have installed python and OBS already, and have the code files downloaded to a folder on your PC.

When I talk about a "script folder", I mean the folder where this Readme and the `src/` directory are placed as well.

1. Open the script folder and run `install-libraries.bat`. This will install all the Python packages we need.
2. Open OBS and go to Tools > Scripts > Python Settings
3. Set the Python Install Path to your Python directory
4. Open the Scripts tab and click "+"
5. Navigate to the script folder and open `leto_theater_reactions.py`

At this point, the script should already start and ask you to enter some info and press the OAuth button.

6. Enter Client ID & Client Secret and press the OAuth button
7. Authorize the script to read your donations and close the tab when done
8. Press the restart button close to the "+" button
9. Add the media sources for the donation animations

## Media Sources

Right now there's 3 media sources to set up:

- "Theater Tip 1 USD" for tips from 1.00 to 4.99 USD
- "Theater Tip 5 USD" for tips from 5.00 to 10.00 USD
- "Theater Tip 10 USD" for tips from 10.00 USD upwards

OBS has limited UI possibilities, so for now just ask me what kind of tiers you want to have and I will adjust the code.
