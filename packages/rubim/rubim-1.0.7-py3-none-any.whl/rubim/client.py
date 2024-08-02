from requests.exceptions import HTTPError , ReadTimeout , ConnectionError
from requests.sessions import Session ; Session = Session()
from .cryption import cryption
from json import dumps,loads
from .config import config
from .tools import tools

class req:

    def __init__(self,auth:str):
        self.auth = auth
        self.enc = cryption(auth)

    def send_request(self,data:dict,method:str,type_method:str="rubino"):

        data.update({"profile_id":config.mainPage["id"]}) if 'profile_id' in data and data['profile_id'] is None else None

        if type_method == "rubino":

            data_json = {
                "api_version": "0",
                "auth": self.auth,
                "client":config.android,
                "data": dumps(data),
                "method": method
            }
            
        elif type_method == "messenger":

            data_json = {
                "api_version": "5",
                "auth": self.auth,
                "data_enc": self.enc.encrypt(
                    dumps({
                        "method": method,
                        "input": data,
                        "client": config.android
                    })
                )
            }

        while True:
            try:
                response = Session.post(
                    url=config.server[type_method],
                    headers=config.headers,
                    json=data_json
                )
            except HTTPError as err:
                raise HTTPError(f"HTTP Error {err.args[0]}")
            except ReadTimeout:
                raise ReadTimeout('Time out')
            except ConnectionError:
                raise ConnectionError('Check your internet connection')
            except:
                continue
            else:
                if 'data_enc' in  response.json():
                    return loads(self.enc.decrypt(response.json()['data_enc']))
                return response.json()
        
    def requestUploadFile(self,size:str,file_type:str,profile_id:str=None):
        return self.send_request({
            "file_name": "rubim.mp4" if file_type == "Video" else "rubim.jpg",
            "file_size": str(size),
            "file_type": file_type,
            "profile_id": profile_id
        },"requestUploadFile")

    def upload(self,post_file:str,profile_id:str=None):

        try:
            file_byte_code = post_file if type(post_file) is bytes else open(post_file,"rb").read()
        except FileNotFoundError:
            raise FileNotFoundError('File Nor Found')

        file_type = tools.getTypeByte(file_byte_code)
        upload_res = self.requestUploadFile(len(file_byte_code),file_type,profile_id)
        if upload_res != None and upload_res["status"] == "OK":
            upload_res = upload_res["data"]
            total_part = len(file_byte_code) // 131072
            upload_data = 0
            for part in range(1, total_part + 2):
                beyte_part = file_byte_code[131072 * (part - 1) : 131072 * part]
                header={
                    "part-number":str(part),
                    "total-part":str(total_part + 1),
                    "auth":self.auth,
                    "hash-file-request":upload_res["hash_file_request"],
                    "file-id":str(upload_res["file_id"]),
                    "content-type": "application/octet-stream",
                    "content-length": str(len(beyte_part)),
                    "Host":upload_res["server_url"].replace("https://","").replace("/UploadFile.ashx",""),
                    "Connection":"Keep-Alive",
                    "accept-encoding": "gzip",
                    "user-agent": "okhttp/3.12.1",
                }
                while True:
                    try:
                        response = Session.post(data=beyte_part,url=upload_res["server_url"],headers=header)
                        if response.status_code == 200:
                            upload_data += round(len(beyte_part) / 1024)
                            print(f"\r{upload_data / 1000} MB | {round(len(file_byte_code) / 1024) / 1000} MB",end="\r")
                            break
                    except ConnectionError:
                        raise ConnectionError('Check your internet connection')
            return (upload_res['file_id'], response.json()["data"]["hash_file_receive"], file_type)
        return upload_res