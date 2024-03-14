source env/bin/activate

# program argument is the date of run (YYYYMMDD) -- e.g. 20240201
# download the dataset
URL="https://dumps.wikimedia.org/other/enterprise_html/runs/$1/enwiki-NS0-$1-ENTERPRISE-HTML.json.tar.gz"
curl -o wiki.json.tar.gz $URL

# this file is NOT held in git repo to avoid it being accidentally run
python3 reset_database.py

cd database_management

# create the term table and middle index
python3 db_fin_script.py

# create the terms json table
python3 json_db_script.py

cd ..

# run pagerank and put results in database
cd pagerank
python3 pagerank.py wiki.json.tar.gz id_file.tsv links_file.csv results_file.tsv
