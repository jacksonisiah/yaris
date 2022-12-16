<img width="150" align="right" alt="yaris" src="https://cdn.discordapp.com/attachments/942564255704682496/1049488483942674452/4d9c3a2aa238aeb4d9f3f8acbe56b869_1.png">

## yaris [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jacksonisiah/yaris/master.svg)](https://results.pre-commit.ci/latest/github/jacksonisiah/yaris/master) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1c8eeecdcc744c65b45003002e0a0d43)](https://www.codacy.com/gh/jacksonisiah/yaris/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jacksonisiah/yaris&amp;utm_campaign=Badge_Grade)

The Discord bot source code behind Chloe which powers Circle People & cats (a personal server).

An overview of the features is available here: [Commands Listing](https://github.com/jacksonisiah/yaris/wiki/Commands)

### using
**With docker compose:**

*  Edit your config file: `$ cp .env.example .env && vi .env`
*  Start with `$ docker compose up -d`

**Manually:**

Requires a valid Python >3.9 environment. You should have Poetry installed.

*  Install dependencies: `$ poetry install` (if you are running on a server, include `--only main`)
*  Edit your config file: `$ cp .env.example .env && vi .env`
*  Run `python main.py`

### contributing

If you have found an issue, you may message me on Discord (Jackson#8026) or open an issue here on GitHub.

Any improvements, especially documentation, type checking, or code quality are welcome. This project uses [poetry](https://python-poetry.org/) to manage dependencies & uses [black](https://github.com/psf/black) code style.
[pre-commit](https://pre-commit.com/) hooks are provided to keep everything tidy, please use them.

### copying
Chloe is licensed under the ISC License, you can do whatever you want as long as you include the original copyright.
See the LICENSE file for details.

Thanks to [NiceAesth](https://github.com/NiceAesth) for helping with various things.
