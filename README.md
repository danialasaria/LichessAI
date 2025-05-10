# LichessAI

> How to beat your friend at chess that always wins:

[![Python 3](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Chess](https://img.shields.io/badge/chess-brightgreen)](https://www.chess.com/)
[![Selenium](https://img.shields.io/badge/selenium-green)](https://www.selenium.dev/)
[![PyAutoGUI](https://img.shields.io/badge/pyautogui-yellow)](https://pyautogui.readthedocs.io/en/latest/)

![lichessAI-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/40123395-86b0-4bce-a46e-1bdc8d78a787)

[▶️ Watch on GitHub](https://github.com/user-attachments/assets/73f7ed01-dc31-4d15-80c0-e1ca62965a6a) • [Original Tweet](https://x.com/danialasaria/status/1804209157379363174)

- [Intro](#intro)
- [Install](#install)
- [Usage](#usage)
- [Parameters](#parameters)
- [License](#license)


## Intro
A python script that automates games on Lichess against your opponents with selenium and pyautogui. There are several flexible parameters including engine source, time control, move speed, account type, and more... ✨


## Install

### Clone Repository
```bash
git clone https://github.com/danialasaria/LichessAI.git
cd LichessAI
```
### Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### Install Dependencies
```bash
pip3 install -r requirements.txt
```

### Download ChromeDriver
Find the chromedriver that matches your computer and visit the corresponding link to download. ChromeDriver works as a bridge between Selenium and Chrome enabling automated control of the browser.
```bash
https://googlechromelabs.github.io/chrome-for-testing/
```

## Usage

### Run 
```
python3 app.py
```
### To stop  
```
Press Control + C
```

## Parameters

### Engine 
Set to Dragon Chess Engine by Komodo but can be replaced with the path to the binary of any engine that follows UCI (Universal Chess Interface) protocol.

EX: Stockfish
```
brew install stockfish
```
```
#find_executable is a function that returns the path to input's executable 
ENGINE_PATH = find_executable('stockfish')
```
### Time Control 
Set to create a challenge of 3 minutes and 0 second increment but can be changed to any time control in Lichess's Quick Pairing.
```
TIME_CONTROL = '3+0'
```
### Move Speed
Set to 0.1 seconds, but can be changed to any duration.
```
ENGINE_ANALYSIS_TIME = .1
```
### Account Mode
Set to anonymous mode, but if ANONYMOUS_MODE is changed to false and username/password filled in, you will be logged in and games will be played on your accounts behalf. 

IMPORTANT NOTE: I don't condone cheating and this is purely for experimental purposes.

```
ANONYMOUS_MODE = True
LICHESS_USERNAME = ''
LICHESS_PASSWORD = ''
```

Feel free to open a PR if you see anything to improve on!

## Debugging
If the cursor is too high/low it is likely you need to adjust the below pixel amount to correspond to your chromium window.
```
DISTANCE_BETWEEN_TOP_OF_SCREEN_AND_LICHESS = 184
```

## License

AGPL v3 © [Danial Asaria](https://danialasaria.com/)

If you found this project interesting, please consider [sponsoring me](https://github.com/sponsors/danialasaria) or <a href="https://twitter.com/danialasaria">following me on twitter <img src="https://storage.googleapis.com/saasify-assets/twitter-logo.svg" alt="twitter" height="24px" align="center"></a>
