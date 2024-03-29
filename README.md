# argofamiglia
An API wrapper created to interface Python with Argo ScuolaNext.
You can use this library to automate some actions like:
- Check for new announcements;
- Check homework for the next and past days;
- And more...

## How the idea was born
The idea was born because the official app doesn't notify you if an announcements arrives, or if you receive a new vote, and also because the app is **REALLY** slow.
I then implemented this API in a [Discord bot](https://github.com/salvatore-abello/ArgoDiscordBot "Discord bot") (not working for now) that notifies me and my class about new announcements from the school.

There are other libraries similar to this one, such as the library created by [Hearot](https://github.com/hearot/ArgoScuolaNext), but it doesn't work anymore. For now this is the only working library.

### How to use
You can install this library with:
`python3 -m pip install -U git+https://github.com/salvatore-abello/argofamiglia.git`

You can also install this from the Python Package Index with:
`python3 -m pip install argofamiglia`


Here's an example of how to obtain a dict containing the homework.
The keys of the dict will be equal to the due dates of the homework.
```
from argofamiglia import ArgoFamiglia

session = ArgoFamiglia("SCHOOL_CODE", "myusername", "mypassword")
print(session.getCompitiByDate())
# prints:
#  {'2022-09-22': {'compiti': ['compiti materia 1',
#                            'compiti materia 2',
#                            'compiti materia 3'],
#                'materie': ['MATERIA 1',
#                            'MATERIA 2',
#                            'MATERIA 3']
# }, ...
```
---
# Disclaimer
This library is not finished, some methods aren't working in the file called `auth.py`
