# get links from keywords
node step_1.js

# prune them and save to json
node step_2.js

# create scrapy project
# move the json there

# crawl all the links
scrapy crawl job_spider > logs.txt

# seperate all into language based json
node step_4.js

# final english filter out for non senior jobs
python3 step_5.py
