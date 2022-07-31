import datetime
import requests
import time
import re
import os

"""
modes: all: params: _dc
docenticlasse --> docenti della classe
bachecanuova --> comunicazioni bacheca
votigiornalieri --> voti
compiti --> compiti
argomenti --> argomenti
verifica --> per testare
login --> login:
schede --> informazioni personali
votigiornalieri --> voti giornalieri
notedisciplinari --> note
assenze --> assenze
orario --> orario
oggi --> Lista di voti, compiti, assenze, etc...
periodiclasse --> scrutinio
votiscrutinio --> voti scrutinio
presavisionebachecanuova --> presa visione di un documento in bacheca:
    params: {'presaVisione': presaVisione, 'prgMessaggio': id}
"""


_vr = re.compile(r"([\d.])+")
_endpoint = "https://www.portaleargo.it/famiglia/api/rest"
_key = "ax6542sdru3217t4eesd9"
_version = "2.1.0"
_app_code = "APF"
_app_company = "ARGO Software s.r.l. - Ragusa"
_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"

class ArgoFamiglia:
    def __init__(self, school, username, password, version=_version):
        self.token = ""
        self.online = False
        self.__school = school
        self.__username = username
        self.__password= password
        self.version = version
        self.connect()

    def connect(self):
        l_req = requests.get(url=f"{_endpoint}/login",
                             headers={
                                "x-key-app": _key,
                                "x-version": self.version,
                                "x-produttore-software": _app_company,
                                "x-app-code": _app_code,
                                "user-agent": _user_agent,
                                "x-cod-min": self.__school,
                                "x-user-id": self.__username,
                                "x-pwd": self.__password
                            },
                            params={
                                "_dc": round(time.time() * 1000)
                            })
        
        if l_req.status_code != requests.codes.ok:
            try:
                self.version = _vr.search(l_req.json()["value"]).group(0)
                self.information = ArgoFamiglia(school, username, password, self.version).informations
                _version = self.version
            except Exception:
                self.online = False
        else:
            self.token = l_req.json()["token"]
            self.online = True
            self.informations = self.getData()[0]


    def getData(self):
        if not self.online:
            return False
        r_schede = requests.get(
            url=_endpoint + "/schede",
            headers={
                "x-key-app": _key,
                "x-version": self.version,
                "x-produttore-software": _app_company,
                "x-app-code": _app_code,
                "user-agent": _user_agent,
                "x-cod-min": self.__school,
                "x-auth-token": self.token
            },
            params={
                "_dc": round(time.time() * 1000)
            }
        )

        return r_schede.json()

    def argoRequest(self, mode, params = dict(), date = datetime.datetime.now().strftime("%Y-%m-%d")): # Send argo requests
        if not self.online:
            return False

        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        params["_dc"] = round(time.time() * 1000)
        if "datGiorno" not in params:
            params["datGiorno"] = date

        request = requests.get(
            url=f"{_endpoint}/{mode}",
            headers={
                "x-key-app": _key,
                "x-version": self.version,
                "user-agent": _user_agent,
                "x-produttore-software": _app_company,
                "x-app-code": _app_code,
                "x-auth-token": self.informations['authToken'],
                "x-cod-min": self.informations['codMin'],
                "x-prg-alunno": str(self.informations['prgAlunno']),
                "x-prg-scheda": str(self.informations['prgScheda']),
                "x-prg-scuola": str(self.informations['prgScuola'])
            },
            params=params
        )
        if request.status_code != requests.codes.ok:
            if request.status_code == requests.codes.not_found:
                return "INVALID_MODE"
            else:
                return "INVALID_CREDENTIALS"
        else:
            return request.json()

    def getUrl(self, prgAllegato, prgMessaggio):
        url = _endpoint + "/messaggiobachecanuova?id=" +\
        self.informations["codMin"].upper().rjust(10, "F")+\
        "II".rjust(5, "E") + str(prgAllegato).rjust(5, "0")+\
        str(prgMessaggio).rjust(10, "0")+\
        self.informations['authToken'].replace("-", "")+\
        _key

        return url

