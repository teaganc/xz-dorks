# Replace GITHUB_NAME and GITHUB_TOKEN with your name and token
sed 's/\(.*\)/mkdir -p repos\/\1 \&\& curl -u GITHUB_NAME:GITHUB_TOKEN https:\/\/api\.github\.com\/repos\/\1\/commits?per_page=1 > repos\/\1\/commits\.json/' githubs.txt > commits_commands.txt

# Github api rate limits to 5000/hr for normal accounts

#head -n 4200 commits_commands.txt | bash
#tail -n +4201 commits_commands.txt | bash
