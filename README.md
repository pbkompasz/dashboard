
## Installation

Clone project  
```
git clone git@github.com:pbkompasz/dashboard.git
cd dashboard/src/
```  
Give permission  
```
sudo chown -R $USER:$USER .
```  
Create `.env` file with database, Stripe, Paypal, etc. tokens (see .env.example)  
Build
```
docker-compose build
```  
Load data  
```
sudo docker-compose run web python manage.py loaddata order/fixtures/status  
sudo docker-compose run web python manage.py loaddata catalog/fixtures/product
```  
Run
```
docker-compose up
```

## Tests

`sudo docker-compose run web python manage.py test`
