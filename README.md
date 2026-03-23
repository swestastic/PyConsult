# PyConsult

PyConsult is the logic and backend of my other project, PiConsult, now with a GUI for desktop use! I built this because I wanted to easily test new features for PiConsult, rather than having to deal with the Pi as a middle man. This also can serve as an alternative to some other common Consult programs, which have historically been Windows only, cost $30-$50 USD, and haven't been updated in 10+ years. PyConsult should, in theory, work on Linux and OS X based systems, although I haven't tested it yet.

This project uses PySerial for ECU connection, NumPy for arrays and data management, and Tkinter for the UI. It should work with most 90's era Nissans, such as the 240sx, 300zx, Skyline, Laurel, etc. So far it has been tested on my two personal cars without issues using a ROM-tuned Z32 VG30DE MT ECU, and a factory S15 SR20DE MT ECU.

## Current Features

- Customizable settings
- Data Stream
- Data Logging to CSV

## Coming Soon

- DTCs (UI is there but no backend)
- Test Mode (UI is there but no backend)
- Data log playback, plotting data logs.

## Usage

Just run `python3 main.py` after changing your working directory to the folder of this repository. This will create a popup window where you can select your USB Consult adapter from the dropdown list, then hit `Connect` to connect to the ECU. 

Calibration settings for units, speed correction (for different differential gears or wheel/tire sizes), and warning thresholds can be altered in `Settings`.

Data readouts can be seen in `Data Stream`.

Settings values are stored in `configJSON.json`.