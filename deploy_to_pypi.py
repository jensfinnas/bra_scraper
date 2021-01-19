#!/usr/bin/env python3
from subprocess import call

# Get current version
with open("VERSION.txt") as f:
    version = f.read().strip()

call(["python3", "setup.py", "sdist", "bdist_wheel"])
call(["python3", "-m", "twine", "upload", "dist/siris_scraper-{}*".format(version)])
