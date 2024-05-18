import json
import requests

class Nobox:
    def __init__(self, token=None):
        self.token = token
        self.result = {
            "Code": 0,
            "IsError": True,
            "Data": None,
            "Error": ""
        }
        self.baseUrl = "https://id.nobox.ai/"

    def generateToken(self, username, password):
        url = self.baseUrl + "AccountAPI/GenerateToken"
        data = {
            "username": username,
            "password": password
        }
        payload = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, data=payload, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            self.result['IsError'] = False
            self.result['Data'] = responseData.get('token')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def uploadFile(self, file):
        url = self.baseUrl + "Inbox/UploadFile/UploadFile"
        files = {'file': (file['name'], open(file['tmp_name'], 'rb'), file['type'])}
        headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.post(url, files=files, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            if responseData.get('Error') is None:
                self.result['IsError'] = False
                self.result['Data'] = responseData.get('Data')
            else:
                self.result['IsError'] = True
                self.result['Error'] = responseData.get('Error')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def uploadBase64(self, filename, mimetype, base64_data):
        url = self.baseUrl + "Inbox/UploadFile/UploadBase64"
        data = {
            'filename': filename,
            'mimetype': mimetype,
            'data': base64_data
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            if responseData.get('Error') is None:
                self.result['IsError'] = False
                self.result['Data'] = responseData.get('Data')
            else:
                self.result['IsError'] = True
                self.result['Error'] = responseData.get('Error')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def sendInboxMessage(self, linkId, channelId, accountIds, bodyType, body, attachment):
        url = self.baseUrl + "Inbox/Send"
        data = {
            "LinkId": linkId,
            "ChannelId": channelId,
            "AccountIds": accountIds,
            "BodyType": bodyType,
            "Body": body,
            "Attachment": attachment
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            if responseData.get('Error') is None:
                self.result['IsError'] = False
                self.result['Data'] = responseData.get('Data')
            else:
                self.result['IsError'] = True
                self.result['Error'] = responseData.get('Error')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def sendInboxMessageExt(self, extId, channelId, accountIds, bodyType, body, attachment):
        url = self.baseUrl + "Inbox/Send"
        data = {
            "ExtId": extId,
            "ChannelId": channelId,
            "AccountIds": accountIds,
            "BodyType": bodyType,
            "Body": body,
            "Attachment": attachment
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            if responseData.get('Error') is None:
                self.result['IsError'] = False
                self.result['Data'] = responseData.get('Data')
            else:
                self.result['IsError'] = True
                self.result['Error'] = responseData.get('Error')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def getChannelList(self):
        url = self.baseUrl + "Services/Master/Channel/List"
        data = {
            'ColumnSelection': 1,
            'IncludeColumns': ['Id', 'Nm']
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            self.result['IsError'] = False
            self.result['Data'] = responseData.get('Entities')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def getAccountList(self):
        url = self.baseUrl + "Services/Nobox/Account/List"
        data = {
            'ColumnSelection': 1,
            'IncludeColumns': ['Id', 'Name', 'Channel']
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            self.result['IsError'] = False
            self.result['Data'] = responseData.get('Entities')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def getContactList(self):
        url = self.baseUrl + "Services/Nobox/Contact/List"
        data = {
            'ColumnSelection': 1,
            'IncludeColumns': ['Id', 'Name']
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=data, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            self.result['IsError'] = False
            self.result['Data'] = responseData.get('Entities')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def fetchLinkList(self, channelId=None, contactId=None):
        url = self.baseUrl + "Services/Chat/Chatlinkcontacts/List"
        request = {
            'IncludeColumns': ["Id", "Name", "IdExt"],
            'ColumnSelection': 1
        }
        
        if channelId or contactId:
            request['EqualityFilter'] = {}
            if contactId:
                request['EqualityFilter']['CtId'] = contactId
            if channelId:
                request['EqualityFilter']['ChId'] = channelId

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.post(url, json=request, headers=headers)
        self.result['Code'] = response.status_code

        if response.status_code == 200:
            responseData = response.json()
            if responseData.get('Error') is None:
                self.result['IsError'] = False
                self.result['Data'] = responseData.get('Entities')
            else:
                self.result['IsError'] = True
                self.result['Error'] = responseData.get('Error')
        else:
            self.result['IsError'] = True
            self.result['Error'] = response.text

        return self.result

    def getTypeList(self):
        bodyTypes = [
            {"text": 'Text', "value": 1},
            {"text": 'Audio', "value": 2},
            {"text": 'Image', "value": 3},
            {"text": 'Sticker', "value": 7},
            {"text": 'Video', "value": 4},
            {"text": 'File', "value": 5},
            {"text": 'Location', "value": 9},
            {"text": 'Order', "value": 10},
            {"text": 'Product', "value": 11},
            {"text": 'VCARD', "value": 12},
            {"text": 'VCARD_MULTI', "value": 13}
        ]

        return bodyTypes
