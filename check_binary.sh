count=0
while read p; do
  printf 'File: %d\n' "$count"
  git clone --no-checkout --depth 1 https://github.com/$p tmp
  git -C tmp ls-tree --full-name --name-only -r HEAD > repos/$p/file.txt
  rm -rf tmp
  (( count ++ ))
done < recent_commits.txt
