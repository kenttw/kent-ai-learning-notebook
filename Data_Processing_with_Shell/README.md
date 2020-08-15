## Please Download File as below
<pre><code>

mkdir data
cd data
mkdir data_processing
cd data_processing
wget https://storage.googleapis.com/kent-share/data_processing/wiki_view_2020_sampling000000000000
wget https://storage.googleapis.com/kent-share/data_processing/wiki_view_2020_sampling000000000001
wget https://storage.googleapis.com/kent-share/data_processing/wiki_view_2020_sampling000000000002
wget https://storage.googleapis.com/kent-share/data_processing/wiki_view_2020_sampling000000000003

wget https://storage.googleapis.com/kent-share/data_processing/title000000000000.json
wget https://storage.googleapis.com/kent-share/data_processing/title000000000001.json
wget https://storage.googleapis.com/kent-share/data_processing/title000000000002.json
wget https://storage.googleapis.com/kent-share/data_processing/title000000000003.json


wget https://storage.googleapis.com/expshare/id_count/id_visit000000000000.txt
wget https://storage.googleapis.com/expshare/id_count/id_visit000000000001.txt
wget https://storage.googleapis.com/expshare/id_count/id_visit000000000002.txt
wget https://storage.googleapis.com/expshare/id_count/id_visit000000000003.txt


</code></pre>

## Please Install Tool as below
<pre><code>
brew install jq
npm install -g gnomon
pip3 install termgraph
pip install doitlive
</code>
</pre>



## Demo as below

<code>
doitlive play find_taiwan_from_wiki_title.sh
</code>
[![asciicast](https://asciinema.org/a/e9L7XVn11fX7ZUVXAfoIywKjU.svg)](https://asciinema.org/a/e9L7XVn11fX7ZUVXAfoIywKjU)

[![asciicast](https://asciinema.org/a/0hsMhLPopjHIj5RdGCYUPyBsf.svg)](https://asciinema.org/a/0hsMhLPopjHIj5RdGCYUPyBsf)

[![asciicast](https://asciinema.org/a/9F7n89RawNW83d1sCb8mG31AR.svg)](https://asciinema.org/a/9F7n89RawNW83d1sCb8mG31AR)