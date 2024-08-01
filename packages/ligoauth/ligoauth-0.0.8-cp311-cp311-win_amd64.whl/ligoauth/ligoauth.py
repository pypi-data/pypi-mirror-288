import requests
import threading

lock = threading.Lock()

baseUrl = "http://www.ligoor.com:8181"
URL_FACTORY_LOGIN = baseUrl + "/rest/camera/factoryLogin"
URL_BATCH_UPLOAD_MAC = baseUrl + "/rest/camera/batchUploadMac"
URL_CHECK_MAC = baseUrl + "/rest/mac/specialAuth"

uid = 0
packageName = ''
companyName = ''
appName = ''


def login(username, pwd):
    with lock:
        data = {
            "userName": username,
            "password": pwd
        }
        url = URL_FACTORY_LOGIN+"?userName="+username+"&password="+pwd
        response = requests.get(url)
        print(url, response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("reuslt", data)
            if data['ret'] == 0 and data["data"]:
                global uid
                global packageName
                global companyName
                global appName
                uid = data["data"]["uid"]
                packageName = data["data"]["packageName"]
                companyName = data["data"]["companyName"]
                appName = data["data"]["appName"]
                return True
        return False


def uploadMac(macs=[]):
    with lock:
        data = {
            "list": macs,
            "packageName": packageName,
            "uid": uid
        }
        response = requests.post(URL_BATCH_UPLOAD_MAC, json=data)
        print(URL_BATCH_UPLOAD_MAC, data, response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("reuslt", data)
            if data["ret"] == 0 and data["data"]["statusCode"] == "101":
                return True
        else:
            print("error", response.text)

        return False


def checkMac(mac):
    with lock:
        url = URL_CHECK_MAC + "?packageName=" + packageName + "&mac=" + mac
        response = requests.get(url)
        print(url, response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("reuslt", data)
            if data["ret"] == 0 and "101" == data["data"]["statusCode"]:
                return True

        return False
