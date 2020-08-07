cd /usr/local/lib/python3.7/site-packages/
find . -name '*google*.py' -print
cat ./google_auth_httplib2.py
find . -name '*google*.py' -print | wc -l
find . -name '*google*.py' -print |xargs cat 
find . -name '*google*.py' -print|xargs cat  | grep  '^from google'
find . -name '*google*.py' -print0 | xargs -0 -n1 -P4 grep '^from google' | wc -l
