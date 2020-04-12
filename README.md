### Clone and Virtual environment
```shell
$ git clone https://github.com/JBthePenguin/MyDiscordBotPython.git
$ cd MyDiscordBotPython
$ virtualenv -p python3 env
$ source env/bin/activate
```

### Requirements
```shell
(env)$ pip install -r requirements.txt
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
- Test for a specific TestCase (ex: CheckerTest)
```shell
(env)$ python -m unittest -v my_bot.info.test.CheckerTest
```
- Only one specific test (ex: test_empty_content)
```shell
(env)$ python -m unittest -v my_bot.info.test.CheckerTest.test_empty_content
```
