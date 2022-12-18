import requests
import datetime
import json
import time

from argofamiglia.CONSTANTS import *
from argofamiglia.auth import codeChallengeLogin, logout, refresh


class ArgoFamiglia:
    def __init__(self, school: str, username: str, password: str):
        self.__school = school
        self.__username = username
        self.__password = password

        self.__token = None
        self.__login_data = None
        self.__headers = {}

        self.connect()

    @property
    def school(self):
        return self.__school

    @property
    def username(self):
        return self.__username

    def update_token(self):
        self.__login_data = refresh(self.__login_data["refresh_token"])

    def connect(self):
        self.__token, self.__login_data = codeChallengeLogin(self.__school, self.__username, self.__password)

        self.__headers = {
            "Content-Type": "Application/json",
            "Authorization": "Bearer " + self.__login_data["access_token"],
            "Accept": "Application/json",
            "x-cod-min": self.__school,
            "x-auth-token": self.__token
        }

        return self

    def request(self, mode: str, request_data: dict = {}) -> dict:
        return requests.post(ENDPOINT + mode, data=request_data, headers=self.__headers).json()

    def getUpdates(self, useExactDatetime=True) -> dict:
        now = datetime.datetime.now()
        return requests.post(ENDPOINT + "dashboard/aggiornadata", headers=self.__headers,
                             json={
                               "dataultimoaggiornamento": now.strftime("%Y-%m-%d %H:%M:%S") if useExactDatetime else f"{now.year}-{now.month}-{now.day} 00:00:00"
                             }
                             ).json()

    def getCompitiByDate(self) -> dict:
        compiti = self.dashboard()["data"]["dati"][0]["registro"]
        date = dict()

        for element in compiti:
            for compito in element["compiti"]:
                if compito["dataConsegna"] not in date:
                    date[compito["dataConsegna"]] = dict()
                    date[compito["dataConsegna"]]["compiti"] = []
                    date[compito["dataConsegna"]]["materie"] = []
                date[compito["dataConsegna"]]["compiti"].append(compito["compito"])
                date[compito["dataConsegna"]]["materie"].append(element["materia"])

        return date

    def dashboard(self, useExactDatetime: bool=True) -> dict:
        now = datetime.datetime.now()
        return requests.post(ENDPOINT + "dashboard/dashboard", headers=self.__headers,
                             json={
                                 "dataultimoaggiornamento": now.strftime("%Y-%m-%d %H:%M:%S") if useExactDatetime else f"{now.year}-{now.month}-{now.day} 00:00:00",
                                 "opzioni": json.dumps(DASHBOARD_OPTIONS)
                             }
                             ).json()

    def getDocumentUrl(self, UID: str) -> str:
        return requests.post(ENDPOINT + "downloadallegatobacheca", headers=self.__headers,
                             json={"uid": UID}).json()["url"]

    def confirmDownload(self, UID: str) -> bool:
        return requests.post(ENDPOINT + "presavisioneadesione", headers=self.__headers,
                             json={"prgMessaggio": UID, "presaVisione": "S"}).json()["success"]
