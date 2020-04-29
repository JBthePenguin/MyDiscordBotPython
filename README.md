[![Build Status](https://travis-ci.com/JBthePenguin/MyDiscordBotPython.svg?branch=master)](https://travis-ci.com/github/JBthePenguin/MyDiscordBotPython) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5f71a237b819419dbb16e46aac038657)](https://www.codacy.com/manual/JBthePenguin/MyDiscordBotPython?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBthePenguin/MyDiscordBotPython&amp;utm_campaign=Badge_Grade) [![python](https://img.shields.io/badge/python-3.7.5-red.svg)](https://www.python.org/downloads/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-red.svg)](https://www.gnu.org/licenses/gpl-3.0) ![GitHub top language](https://img.shields.io/github/languages/top/JBthePenguin/MyDiscordBotPython) ![GitHub repo size](https://img.shields.io/github/repo-size/JBthePenguin/MyDiscordBotPython)
## MyDiscordBotPython

***IN PROGRESS***

### Install

#### Clone and Virtual environment
```shell
$ git clone https://github.com/JBthePenguin/MyDiscordBotPython.git
$ cd MyDiscordBotPython
$ virtualenv -p python3 env
$ source env/bin/activate
```

#### Requirements and Discord token
- [discord.py](https://discordpy.readthedocs.io/en/latest/) - [python-dotenv](https://github.com/theskumar/python-dotenv) - [aiounittest](https://github.com/kwarunek/aiounittest) - [tinydb](https://tinydb.readthedocs.io/en/latest/)
```shell
(env)$ pip install -r requirements.txt
```
- create a *.env* file and replace *HereYourToken* with your personnal discord bot token
```shell
(env)$ echo "DISCORD_TOKEN=HereYourToken" > .env
```

### Run
- Full bot
```shell
(env)$ python my_bot
```
- Info Team bot
```shell
(env)$ python my_bot --info
# or
(env)$ python my_bot -i
```
- Event bot
```shell
(env)$ python my_bot --event
# or
(env)$ python my_bot -e
```

### Tests
- All tests
```shell
(env)$ python -m unittest -v
```
- Test for a specific module (ex: info)
```shell
(env)$ python -m unittest -v my_bot.info.test
```
- Test for a specific TestCase (ex: InfoGuildCommandsTest)
```shell
(env)$ python -m unittest -v my_bot.info.test.InfoGuildCommandsTest
```
- Only one specific test (ex: test_members)
```shell
(env)$ python -m unittest -v my_bot.info.test.InfoGuildCommandsTest.test_members
```

### Screenshots
![Info Guild Commmands](screenshots/infoguildcommands.png)
