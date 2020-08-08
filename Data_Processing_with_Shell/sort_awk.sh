#doitlive speed: 3
curl https://data.wa.gov/api/views/tgdf-dvhm/rows.csv\?accessType\=DOWNLOAD | more
curl https://data.wa.gov/api/views/tgdf-dvhm/rows.csv\?accessType\=DOWNLOAD | sort
curl https://data.wa.gov/api/views/tgdf-dvhm/rows.csv\?accessType\=DOWNLOAD | awk -F, '{print $1}'
curl https://data.wa.gov/api/views/tgdf-dvhm/rows.csv\?accessType\=DOWNLOAD | awk -F, '{print $2}' | sort
curl https://data.wa.gov/api/views/tgdf-dvhm/rows.csv\?accessType\=DOWNLOAD | awk -F, '{print $2}' | sort | uniq -c | sort -nr

