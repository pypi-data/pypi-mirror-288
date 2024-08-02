import os
import json
from .fd_httpclient import FDHttpClient
from .chat._client import FourthDimensionAI
from .fd_utils import *
fdHttpClient = FDHttpClient()
package_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
resource_path = os.path.join(package_path, "resources")
config_path = os.path.join(resource_path, "fd_python_config.json")

class FDClient:
    def __init__(self):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.Baseurl = self.config["url"]["base_url"] + "/"
        self.CHUNK_EMBEDDING = 0x01
        self.SENTENCE_EMBEDDING = 0x02
        self.SUMMARIZING = 0x08
        self.CHUNK_SUMMARIZING = 0x10
        self.SELF_ASKING = 0x04
        # self.CHUNK_SELF_ASKING = 0x20

    def setServeUrl(self, serve_url):
        """用于设置BaseUrl"""
        self.Baseurl = serve_url + "/"

    def getKBInfo(self, KBName):
        """用于获取知识库信息"""
        requestdata = create_dict_from_kwargs(kbName=KBName)
        result = fdHttpClient.send_request(url=self.Baseurl + "getKBInfo", json_data=requestdata, method="POST")
        return result

    def createKB(self, KBName):
        """用于创建知识库"""
        requestdata = create_dict_from_kwargs(kbName=KBName)
        result = fdHttpClient.send_request(url=self.Baseurl + "createKB", json_data=requestdata, method="POST")
        print(result["msg"] )
        return result

    def deleteKB(self, KBName):
        """用于删除知识库"""
        requestdata = create_dict_from_kwargs(kbName=KBName)
        result = fdHttpClient.send_request(url=self.Baseurl + "deleteKB", json_data=requestdata, method="POST")
        print(result["msg"] )
        return result

    def importDocuments(self, KBName, targetFileName, rumination):
        """用于导入文件夹"""
        print("开始文件的导入")
        Document_list = get_all_file_paths(targetFileName)
        for Document_Path in Document_list:
            files = {"file": open(Document_Path, "rb")}
            requestdata = create_dict_from_kwargs(kbName=KBName, targetFileName=Document_Path, rumination=rumination)
            result = fdHttpClient.send_request_fromdata(url=self.Baseurl + "addDocument", data=requestdata, files=files, method="POST")
            print(Document_Path + result["msg"])
        result["msg"] = "文件夹导入成功"
        return result

    def addDocument(self, KBName, targetFileName, rumination):
        """用于添加文档"""
        files = {"file": open(targetFileName, "rb")}
        requestdata = create_dict_from_kwargs(kbName=KBName, targetFileName = targetFileName, rumination=rumination)
        result = fdHttpClient.send_request_fromdata(url=self.Baseurl + "addDocument", data=requestdata ,files = files,method="POST")
        print(result["msg"] )
        return result

    def deleteDocument(self, KBName, targetFileName):
        """用于删除文档"""
        requestdata = create_dict_from_kwargs(kbName=KBName, targetFileName=targetFileName)
        result = fdHttpClient.send_request(url=self.Baseurl + "deleteDocument", json_data=requestdata, method="POST")
        print(result["msg"] )
        return result

    def updateDocument(self, KBName, sourceFileName, targetFileName, rumination):
        """用于更新文档"""
        DeleteFileName = os.path.basename(sourceFileName)
        requestdata = create_dict_from_kwargs(kbName=KBName, targetFileName=sourceFileName)
        fdHttpClient.send_request(url=self.Baseurl + "deleteDocument", json_data=requestdata, method="POST")
        files = {"file": open(targetFileName, "rb")}
        requestdata = create_dict_from_kwargs(kbName=KBName, targetFileName = targetFileName, rumination=rumination)
        result = fdHttpClient.send_request_fromdata(url=self.Baseurl + "addDocument", data=requestdata ,files = files,method="POST")
        print("更新成功" + "\n")
        return result

    def recallDocuments(self, KBName, question):
        """用于查询"""
        requestdata = create_dict_from_kwargs(kbName=KBName, question=question)
        result = fdHttpClient.send_request(url=self.Baseurl + "recall", json_data=requestdata, method="POST")
        print(result["msg"])
        return result

    def query(self, KBName, question):
        """获取查询和生成回答"""
        client = FourthDimensionAI(base_url=self.Baseurl)
        result = client.chat.completions.create(
            model="qwen",
            question=question,
            kbName=KBName,
            messages=[]
        )
        return result.data

    def ruminate(self, KBName, rumination):
        """用于反刍"""
        requestdata = create_dict_from_kwargs(kbName=KBName, rumination=rumination)
        result = fdHttpClient.send_request(url=self.Baseurl + "ruminate", json_data=requestdata, method="POST")
        print(result["msg"])
        return result

