find  t*.json  | xargs -n1 -P4   jq .en_description |grep taiwan  | wc -l | gnomon
