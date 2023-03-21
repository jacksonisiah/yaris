### yaris [[Commands Listing](https://github.com/jacksonisiah/yaris/wiki/Commands)]
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jacksonisiah/yaris/master.svg)](https://results.pre-commit.ci/latest/github/jacksonisiah/yaris/master) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/1c8eeecdcc744c65b45003002e0a0d43)](https://www.codacy.com/gh/jacksonisiah/yaris/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jacksonisiah/yaris&amp;utm_campaign=Badge_Grade)

The code behind Chloe supporting operations in cats & Circle People. Supports unique features like Reminders with more to come.

### setup
**Dependencies**
- python 3.9+
- postgres 15+
- python-poetry
- docker (optional)

Copy the environment file and populate `.env` with your configuration.

Install dependencies with `poetry install` (include `--only main` on servers)

**Database setup & migrations**
```
postgres# create user chloe_user with password 'changeme' createdb; createdb chloe;
```
Run `aerich migrate` to run all neccessary migrations. (if on docker this is already done for you)

**Startup**

Run `python3 main.py` to start the bot process.

### license & thanks
ISC

Thanks to [NiceAesth](https://github.com/NiceAesth) for helping with various things.
