import base64
import requests
import os
from dotenv import load_dotenv
from github import Github
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
        self.g = Github(token)
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
        try:

            #new_data = base64.b64encode(new_data.encode('utf-8')).decode('utf-8')
            repo = self.g.get_repo(user + '/' + self.repo)
            readme_file = repo.get_contents("README.md")
            print(self.data['sha'])
            repo.update_file(
                path='README.md',
                message="15th Nov 2025",
                content=new_data,
                sha=readme_file.sha,
                branch='main'
            )
            print("The readme was updated")
        except:
            print("An error occurred")

    def update_about(self,content):
        try:
            repo = self.g.get_repo(user + '/' + self.repo)
            repo.edit(
                description=content
            )
            print("The about was updated")
        except Exception as e:
            print(repo.permissions)
            print("An error occurred: ",str(e))

    

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


if __name__ == "__main__":
    readme = Readme("multi-agent-dev-marketing-system")
    readme.update_about("test")