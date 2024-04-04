if [ ! -d "./gentoo" ]; then 
  echo "Cloning Git Repo:"
  git clone https://anongit.gentoo.org/git/repo/gentoo.git --depth 1
else 
  echo "Using Git Repo: ./gentoo"
fi

echo "Package Count:"
find ./gentoo/ -name "Manifest" | wc -l

if [ ! -f "./dependency.txt" ]; then
  echo "Outputting dependency.txt"
  python3 dependency.py > dependency.txt
else 
  echo "Using dependency.txt"
fi


if [ ! -f "./githubs.txt" ]; then 
  echo "Outputting githubs.txt"
  sed 's/^/gentoo\//' dependency.txt | sed 's/\W:\W[0-9]*$/\/metadata.xml/' | xargs grep -hsm 1 "type=\"github\"" | sed 's/\W*<remote-id type=\"github\">//' | sed 's/<\/remote-id>//' > githubs.txt
else 
  echo "Using githubs.txt"
fi

echo "Github Count:"
cat githubs.txt | wc -l
