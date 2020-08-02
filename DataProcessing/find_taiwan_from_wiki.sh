#doitlive speed: 3
cd /Users/kent/git/aiacademy-learning-notebook/DataProcessing/data/data_processing
ls -alh titl*
cat title000000000000.json | more
find title* | xargs cat | wc -l
find titl* | xargs jq . | more
find titl* | xargs jq .en_description | more
find titl* | xargs jq .en_description | grep taiwan | more
find titl* | xargs -n1 -P4 jq .en_description | grep taiwan | more
find titl* | xargs -n1 -P4 jq .en_description | grep taiwan | wc -l
