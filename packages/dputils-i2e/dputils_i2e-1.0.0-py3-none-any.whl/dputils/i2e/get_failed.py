import re

REGEX = re.compile(r".*===> Failed with (.*) - (.*)$")


with open("r.log", 'rt') as f:
    for line in f:
        if match := REGEX.match(line.strip()):
            print(tuple(reversed(match.groups())), ',', sep='')


