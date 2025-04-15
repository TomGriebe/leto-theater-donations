# Leto Theater Reactions

Allows you to queue animations for incoming donations.
The animations will wait for your idle loop to finish, so you can properly blend between them.

## Installing Python

OBS scripts need Python to run, so you will need to install it, if you haven't already.

To check if you have an installation of Python, open your Terminal and run `python --version`. If you get an error, you don't have it.

You can find the instructions on the official [Python website](https://www.python.org/downloads/).

## Media Sources

Right now there's 4 media sources to set up. They need to be named exactly like this:

- "Theater Idle"
- "Theater Tip 1 USD" for tips from 1.00 to 4.99 USD
- "Theater Tip 5 USD" for tips from 5.00 to 10.00 USD
- "Theater Tip 10 USD" for tips from 10.00 USD upwards

OBS has limited UI possibilities, so the price ranges have to be adjusted in the code. I've tried to make it as simple as possible, you should just have to touch the list at the top of the `sources.py` file:

```python
sources = [
    {"name": "Theater Tip 1 USD", "from": 0, "to": 5},
    {"name": "Theater Tip 5 USD", "from": 5, "to": 10},
    {"name": "Theater Tip 10 USD", "from": 10, "to": MAX_DONATION},
]
```

For example, "Theater Tip 1 USD" will be triggered by donations from $0 to $4.99 (higher or equal to 0, lower than 5).

You can hide the tip sources in a folder, the important thing is that the names match.

## Initial Setup

These steps assume that you have installed Python and OBS already, and have the code files downloaded to a folder on your PC.

When I talk about a "script folder", I mean the folder where this Readme and the `src/` directory are placed as well.

1. Create [Media Sources](#media-sources)
2. Open the script folder and run `install-libraries.bat`. This will install all the Python packages we need.
3. Open OBS and go to Tools > Scripts > Python Settings
4. Set the Python Install Path to your Python directory
5. Open the Scripts tab and click "+"
6. Navigate to the script folder and open `leto_theater_reactions.py`

At this point, the script should already start and ask you to enter some info and press the OAuth button.

7. Enter Client ID & Client Secret and press the OAuth button
8. Authorize the script to read your donations and close the tab when done
9. Press the restart button close to the "+" button
10. Add the media sources for the donation animations

Whenever you make changes in the code, like adjusting the tip tiers, you need to either restart OBS, or press the script reload button again, like in step 9.
