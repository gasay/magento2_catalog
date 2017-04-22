echo "Path: "$1;
(cd $1 && for i in `find . -type f | grep -v \.git | grep -v \.DS_Store | grep -v "^.$" | grep -v "modman" | grep -v "composer.json" | grep -v \.txt | grep -v \.pdf | sed 's/\.\///'`; do echo ${i} ${i}; done > modman;)
