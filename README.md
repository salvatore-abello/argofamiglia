# Argo Famiglia API (Not working as of September 2022, for now)
A library created to interface Python with Argo ScuolaNext.
You can use this library to automate some actions like:
- Check for new announcements;
- Check homework for the next and past days;
- And more...

## How the idea was born
The idea was born because the official app doesn't notify you if an announcements arrives, or if you receive a new vote, and also because the app is **REALLY** slow.
I then implemented this API in a [Discord bot](https://github.com/salvatore-abello/ArgoDiscordBot "Discord bot") that notifies me and my class about new announcements from the school.

I then discovered that there are libraries already developed by others that do the exact same thing. [hearot](https://github.com/hearot/) has developed a much better library than mine, [it's worth checking out](https://github.com/hearot/ArgoScuolaNext). Thanks to him, I improved some things about my library.

### How to use
You can install this library with:
`python3 -m pip install -U git+https://github.com/salvatore-abello/ArgoFamigliaAPI.git`

You can also install this from the Python Package Index with:
`python3 -m pip install argofamiglia`


Below is an example of how to print announcements.
```
from argofamiglia import ArgoFamiglia

session = ArgoFamiglia("SCHOOL_CODE", "myusername", "mypassword")
print(session.argoRequest("bachecanuova"))
```

## DISCLAIMER
Use this library at your own risk, as it violates the following terms of the services:

```The authentication token and the restful services invoked through it, can only be used by the "DidUP - Famiglia" application of Argo Software SRL for the provision of its services or by saas suppliers and related applications specifically pre-authorized, in compliance with current legislation in manner of protection of personal data and the measures required by the AgID for the SaaS applications of the PA.```

```Il token di autenticazione e i servizi restful invocati mediante esso, possono essere utilizzati solo dall'applicazione "DidUP - Famiglia" della Argo Software SRL per l’erogazione dei propri servizi o da fornitori saas e relative applicazioni appositamente preautorizzate, in conformità alla vigente normativa in maniera di protezione dei dati personali ed alle misure richieste dall'AgID per gli applicativi SaaS delle PA.```

## Credits
Thanks to [veetaw](https://github.com/veetaw/), as I took inspiration (and even help) [from his unofficial client](https://github.com/veetaw/argo-scuolanext-dart).



