- conda create -n [env_name]
- conda activate [env_name] 
- conda install scrapy
- scrapy startproject [proj_name]
- cd [proj_name]
- scrapy genspider [spider_name] [domain]
- scrapy crawl [spider_name] -a keyword="[keyword]"