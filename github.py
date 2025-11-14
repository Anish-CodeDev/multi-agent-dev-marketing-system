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
        self.headers = {"Authorization": f"token {token}",
                        "Accept": "application/vnd.github+json"}
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
        _ = self.load_readme()
        update_data = {
        "message": "Update README",
        "content": new_data,
        "sha": self.data["sha"],
        "branch":"main"               # required to update
        }

        response = requests.put(url=self.url,headers=self.headers,json=update_data)

        if response.status_code == 200 or response.status_code == 201:
            print("✅ README updated successfully!")
            return "good"
        else:
            print("❌ Failed to update:",response.status_code)
            return "bad"
    

def list_repos(username):
    page = 1
    repos = []
    url = f"https://api.github.com/users/{username}/repos"

    while True:
        response = requests.get(url=url,params={"per_page":100,"page":page})
        data = response.json()

        if not data:
            break
        page+=1
        print(data)
        repos.extend([repo['name'] for repo in data])

    return repos        

def get_stars(username):
    starred = {}
    page = 1
    url = f"https://api.github.com/users/{username}/repos"

    while True:
        response = requests.get(url=url,params={"per_page":100,'page':page})
        data = response.json()

        if not data:
            break
        page+=1

        for repo in data:
            starred[repo['name']] = repo['stargazers_count']
    
    return starred

