# binaexperts/vitrine.py
import requests
import base64
from tkinter import Tk
from tkinter.filedialog import askopenfilename

BASE_URL = 'https://py-api.devbina.ir/api/v2/'
AUTH_URL = BASE_URL + 'user/auth/token/'
ORG_ID = 15
IMPORT_URL = BASE_URL + 'core/' + str(ORG_ID) + '/datasets/import/'
class Vitrine:
    def __init__(self, username='', password='', org_id = 15):
        if not username:
            username = input('enter your username: ')
        if not password:
            password = input('enter your username: ')
        self.username = username
        self.password = password
        self.org_id = org_id
        self.url = BASE_URL + 'core/' + str(org_id) + '/datasets/import/' 
        self.token = self.login()

    def login(self):
        auth_data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(AUTH_URL, json=auth_data)
        if response.status_code == 200:
            token = response.json().get('token')
            return token
        else:
            print("Failed to log in. Status code:", response.status_code)
            return None

    def encode_file_to_base64(self, file_path):
        with open(file_path, 'rb') as file:
            encoded_file = 'data:@file/zip;base64,' + base64.b64encode(file.read()).decode('utf-8')
        return encoded_file

    def import_file(self, encoded_file, dataset_name, dataset_type):
        headers = {'Authorization': f'JWT {self.token}'}
        import_data = {
            'zip_file': encoded_file,
            'dataset_name': dataset_name,
            'dataset_type': dataset_type
        }
        response = requests.post(self.url, headers=headers, json=import_data)
        if 200 <= response.status_code < 300:
            print("File imported successfully.")
            return response
        else:
            print("Failed to import file. Status code:", response.status_code)
            return response
    
    def upload(self, file_path: str, dataset_name: str="default_dataset_name", dataset_type: str="object-detection"):
        if self.token:
            encoded_file = self.encode_file_to_base64(file_path)
            response = self.import_file(encoded_file, dataset_name, dataset_type)
            if response.status_code == 204:
                print('uploaded')
                return True
        return False

    def select_upload(self):
        dataset_name = input('enter your project/dataset name: ')
        dataset_type_id = input('enter your project type:\nobject_detection = 0\ninstance_segmentation = 1\nclassification= 2\n: ')
        if dataset_type_id == '0':
            dataset_type = 'object-detection'
        elif dataset_type_id == '1':
            dataset_type = 'segmentation'
        else:
            dataset_type = 'classification'
        self.upload(self.select_file())
        
    @staticmethod
    def select_file():
        # Create a Tk root widget and hide it
        root = Tk()
        root.withdraw()

        # Use a file dialog to select the file
        file_path = askopenfilename(title="Select a ZIP file", filetypes=[("ZIP files", "*.zip")])
        if not file_path:
            print("No file selected.")
            return None
        return file_path
    
