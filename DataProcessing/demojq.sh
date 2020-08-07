#doitlive speed: 3

curl https://api.covidtracking.com/v1/us/daily.json | more
curl https://api.covidtracking.com/v1/us/daily.json | jq | more
curl https://api.covidtracking.com/v1/us/daily.json | jq '.[].date' > usa_date.txt
head  usa_date.txt
curl https://api.covidtracking.com/v1/us/daily.json | jq '.[].positive' > usa_positive.txt
head  usa_positive.txt

paste usa_date.txt usa_positive.txt  | tail -r  | termgraph --color {red,green}
