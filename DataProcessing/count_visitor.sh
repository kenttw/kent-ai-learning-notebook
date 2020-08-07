cd ./data/data_processing/
cat *id*.txt | more
cat *id*0.txt | sort |  more
cat *id*0.txt | sort | uniq -c |more
cat *id*0.txt | sort | uniq -c | sort -nr |more


cat *id*.txt | sort |uniq -c | sort -nr | gnomon > id_sort.txt
