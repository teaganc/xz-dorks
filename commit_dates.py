import datetime
import json 
import re

def main():
    with open("contrib_top.txt") as f:
        packages = f.read().strip().split('\n')
        
    with open("recent_commits.txt", "w") as f:
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=365)
        for package in packages:
            try:
                with open("./repos/" + package.strip() + "/commits.json") as commit:
                    dct = json.loads(commit.read())
                    date_str = dct[0]["commit"]["author"]["date"]
                    date = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                    if date > cutoff_date:
                        print(package, file=f)
            except:
                pass


main()

