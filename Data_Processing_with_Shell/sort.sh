#doitlive speed: 3

curl https://corona-virus-stats.herokuapp.com/api/v1/cases/countries-search
curl https://corona-virus-stats.herokuapp.com/api/v1/cases/countries-search | jq '.data' | more
curl https://corona-virus-stats.herokuapp.com/api/v1/cases/countries-search | jq '.data.rows[].total_cases'
curl https://corona-virus-stats.herokuapp.com/api/v1/cases/countries-search | jq '.data.rows[].country'

paste cov_coutnry.txt  cov_case.txt
paste cov_coutnry.txt  cov_case.txt | sed "s/\"//g"
paste cov_coutnry.txt  cov_case.txt | sed "s/\"//g" | sed "s/,//g"
paste cov_coutnry.txt  cov_case.txt | sed "s/\"//g" | sed "s/,//g" | sort
paste cov_coutnry.txt  cov_case.txt | sed "s/\"//g" | sed "s/,//g" | sort -n
paste cov_coutnry.txt  cov_case.txt | sed "s/\"//g" | sed "s/,//g" | sort -nr -k 1
paste cov_coutnry.txt  cov_case.txt | sed "s/\"//g" | sed "s/,//g" | sort -nr -k 2