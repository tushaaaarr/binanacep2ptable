# c25-market

After Cloning project Follow below steps

Modify .env file with at
```
c25-market/c25-market/.env
```

run the following commands (on project base directory) 
```
python manage.py makemigrations
python manage.py migrate
python manage.py search_index --rebuild
```

Run the following command to start Elasticsearch from the command line (on elasticsearch/bin 
```
elasticsearch.
```

Run the following command to start Django Project
```
python manage.py runserver
```

Goto following URL to apply initial database operations
```
<HOST>/setup_elastic_search
```

Run the following command to start Scrapper file (on scrapper folder)
```
python scrapper.py
```