import base64
import requests
import os
from dotenv import load_dotenv
user = 'Anish-CodeDev'
load_dotenv()
token = os.environ['GITHUB_TOKEN']

class Readme:

    def __init__(self,repo):
        self.repo = repo
        self.url = f"https://api.github.com/repos/{user}/{repo}/contents/README.md"
        self.data = {}
        self.headers = None
    def load_readme(self):


        
        self.headers = {"Authorization":f"token {token}"}

        response = requests.get(headers=self.headers,url=self.url)
        self.data = response.json()
        #print(self.data)
        try:

            content = base64.b64decode(self.data['content']).decode('utf-8')
        #print(content)
            return content
        except KeyError as e:
            return "An error occurred"

    def update_readme(self,new_data):
        new_data = base64.b64encode(new_data.encode('utf-8')).decode('utf-8')

        update_data = {
        "message": "Update README",
        "content": new_data,
        "sha": self.data["sha"]  # required to update
        }

        response = requests.put(url=self.url,headers=self.headers,json=update_data)

        if response.status_code == 200 or response.status_code == 201:
            print("✅ README updated successfully!")
            return "good"
        else:
            print("❌ Failed to update:")
            return "bad"

readme = Readme("Desktop_AI_Agent")
print(readme.load_readme())

