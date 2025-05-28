import base64
import csv
import json
import os
import pathlib
import platform
import random
import string
from dataclasses import asdict, dataclass, fields
from datetime import datetime, timedelta

import requests


class ItemProcessor:
    def write_as_sql(self) -> str:
        clean_list = []
        for field in fields(self):
            if field.type is list:
                clean_list.append(f"ARRAY{getattr(self, field.name)}")
            elif field.type is str:
                try:
                    clean_list.append(getattr(self, field.name).replace("'", ""))
                except AttributeError as e:
                    # print(e)
                    # clean_list.append("NULL")
                    clean_list.append("")
            else:
                clean_list.append(getattr(self, field.name))

        sql_syntax = tuple(clean_list)
        return str(sql_syntax).replace('"', "")

    def write_to_csv(self) -> dict:
        # Replace [] for {} due to SQL import syntax error for array columns.
        keys = (field.name for field in fields(self))
        values = (
            (
                set(getattr(self, field.name))
                if field.type is list
                else getattr(self, field.name)
            )
            for field in fields(self)
        )
        csv_syntax = {k: v for k, v in zip(keys, values)}
        return csv_syntax

    def get_field_names(self) -> list:
        return [field.name for field in fields(self)]

    def format_date(date_string) -> str:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y")


class DataProcessor:
    def save_data_to_sql(self, schema, sql_folder_path) -> None:
        for field in fields(self):
            file_name = os.path.join(sql_folder_path, f"{schema}-{field.name}.sql")
            baseSql = f"INSERT INTO {schema}.{field.name} {str(tuple(key for key in getattr(self, field.name)[0].get_field_names())).replace("'", "")} VALUES"
            sqlData = [item.write_as_sql() for item in getattr(self, field.name)]

            with open(file_name, "w", newline="", encoding="utf-8") as sqlFile:
                sqlFile.seek(0)
                sqlFile.write("{}\n".format(baseSql))
                for i, row in enumerate(sqlData, start=1):
                    if i != len(sqlData):
                        sqlFile.write("{},\n".format(row))
                    else:
                        sqlFile.write("{};".format(row))

    def save_data_to_csv(self, csv_folder_path):
        for field in fields(self):
            file_name = os.path.join(csv_folder_path, f"{field.name}.csv")
            csv_headers = [
                key for key in getattr(self, field.name)[0].get_field_names()
            ]
            csv_data = [item.write_to_csv() for item in getattr(self, field.name)]

            with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
                writer.writeheader()
                writer.writerows(csv_data)

    def save_data_to_json(self, json_folder_path) -> None:
        for field in fields(self):
            file_name = os.path.join(json_folder_path, f"{field.name}.json")
            json_data = [asdict(item) for item in getattr(self, field.name)]

            with open(file_name, "w", encoding="utf-8") as jsonFile:
                jsonFile.seek(0)
                json.dump(json_data, jsonFile, indent=4, sort_keys=True)
                jsonFile.truncate()


@dataclass
class LogItem(ItemProcessor):
    data_items: int
    description: str
    finished: str
    project_name: str
    start: str
    status_code: int
    task_id: str
    task_name: str

    def generate_id():
        characterList = string.ascii_letters + string.digits
        myId = "".join([random.choice(characterList) for i in range(30)])
        return myId

    def format_date(self):
        return self.start.strftime("%Y-%m-%d %H:%M:%S")
        # return self.start.strptime("%Y-%m-%d %H:%M:%S")

    def __init__(self, project_name, task_name):
        self.data_items = 0
        self.description = None
        self.finished = None
        self.project_name = project_name
        self.start = datetime.now()
        self.status_code = None
        self.task_id = LogItem.generate_id()
        self.task_name = task_name

    def __str__(self):
        return f"{self.project_name} - {self.task_name} (id: {self.task_id}) on {self.start}: {self.error_message} "

    def log_actions(self, data_items=0, description="Success", status_code=200) -> None:
        self.data_items = data_items
        self.description = description
        self.status_code = status_code
        self.finished = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.start = self.format_date()
        print("Log saved.")


class Authenticator:
    def loadJson(path=None, account=None):
        jsonFile = json.load(open(path, "r"))
        return jsonFile[account]

    def __init__(self, account):
        self.account = account
        if platform.system() == "Windows":
            self.path = os.path.join(
                pathlib.Path(__file__).parent.parent.resolve(),
                "assets",
                "credentials.json",
            )
        else:
            self.path = os.path.join(
                pathlib.Path(__file__).parent.parent.resolve(),
                "assets",
                "credentials.json",
            )
        self.today = datetime.now()
        self.keys = Authenticator.loadJson(path=self.path, account=self.account)

    def getClientId(self):
        return self.keys["CLIENT_ID"]

    def getClientSecret(self):
        return self.keys["CLIENT_SECRET"]

    def getCode(self):
        return self.keys["CODE"]

    def getAccessToken(self):
        return self.keys["ACCESS_TOKEN"]

    def getExpiryDate(self):
        return self.keys["EXPIRY_DATE"]

    def getGrantType(self):
        return self.keys["GRANT_TYPE"]

    def getRefreshToken(self):
        return self.keys["REFRESH_TOKEN"]

    def getRefreshTokenUrl(self):
        return self.keys["TOKEN_URL"]

    def getHeaders(self):
        headers = {
            "Authorization": f"Bearer {self.getAccessToken()}",
            "Content-Type": "application/json",
        }
        return headers

    def isTokenExpired(self) -> bool:
        expiryDate = datetime.strptime(self.keys["EXPIRY_DATE"], "%Y-%m-%d %H:%M:%S")
        if expiryDate < self.today:
            return True

    def saveJson(self):
        with open(self.path, "r+") as jsonFile:
            data = json.load(jsonFile)
            data[self.account] = self.keys
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4, sort_keys=False)
            jsonFile.truncate()

    def RequestRefreshToken(self):
        log_item = LogItem(
            project_name=f"auth-{self.account.lower()}",
            task_name=self.RequestRefreshToken.__name__,
        )
        isTokenExpired = self.isTokenExpired()
        if isTokenExpired:
            # SPOTIFY
            if self.account == "SPOTIFY":
                auth_client = self.getClientId() + ":" + self.getClientSecret()
                auth_encode = "Basic " + base64.b64encode(auth_client.encode()).decode()
                payload = {
                    "grant_type": "refresh_token",
                    "refresh_token": self.getRefreshToken(),
                    # "client_id": self.getClientId(),
                    "code": self.getCode(),
                }
                headers = {"Authorization": auth_encode}
                url = self.getRefreshTokenUrl()
                r = requests.post(url=url, headers=headers, data=payload)
            # STRAVA
            elif self.account == "STRAVA":
                payload = {
                    "grant_type": "refresh_token",
                    "client_id": self.getClientId(),
                    "client_secret": self.getClientSecret(),
                    "refresh_token": self.getRefreshToken(),
                }
                url = self.getRefreshTokenUrl()
                r = requests.post(url=url, data=payload)

            if r.status_code == 200:
                response = r.json()
                expires_in = response["expires_in"]
                new_expiry_date = self.today + timedelta(seconds=expires_in)

                # Updating keys
                self.keys["ACCESS_TOKEN"] = response["access_token"]
                self.keys["EXPIRY_DATE"] = new_expiry_date.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    self.keys["SCOPE"] = response["scope"]
                    self.keys["REFRESH_TOKEN"] = response["refresh_token"]
                except:
                    pass
                # Saving to database.
                self.saveJson()
                print("Access token refreshed.")
                log_item.log_actions(
                    data_items=0, description=r.reason, status_code=200
                )
                return log_item
            else:
                print(r.json())
                log_item.log_actions(
                    data_items=0,
                    description=r.reason,
                    status_code=r.status_code,
                )
                return log_item
        else:
            log_item.log_actions(
                data_items=0,
                description="OK",
                status_code=200,
            )
            return log_item
