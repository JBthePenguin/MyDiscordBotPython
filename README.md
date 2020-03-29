### Clone and Virtual environment
```shell
$ git clone https://github.com/JBthePenguin/MyDiscordBotPython.git
$ cd MyDiscordBotPython
$ virtualenv -p python3 env
$ source env/bin/activate
```

### Requirements
```shell
(env)$ pip install -U discord.py
(env)$ pip install -U python-dotenv
(env)$ pip install tinydb
```

### Run
- Full bot
```shell
(env)$ python full_bot
```
- Info Team bot
```shell
(env)$ python info_team_bot
```
- Calendar bot
```shell
(env)$ python calendar_bot
```