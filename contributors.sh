# Replace GITHUB_NAME and GITHUB_TOKEN with your name and token
sed 's/\(.*\)/mkdir -p repos\/\1 \&\& curl -u GITHUB_NAME:GITHUB_TOKEN https:\/\/api\.github\.com\/repos\/\1\/contributors > repos\/\1\/contributors\.json/' githubs.txt > contributors_commands.txt

# Github api rate limits to 5000/hr for normal accounts

#head -n 4200 contributors_commands.txt | bash
#tail -n +4201 contributors_commheadands.txt | bash
