
## Run 

- Create project
`sudo docker compose run web django-admin startproject composeexample .`
- Give permissions
`sudo chown -R $USER:$USER composeexample manage.py`
- Create `.env` file with database, Stripe, Paypal, etc. tokens

## Load data

`sudo docker-compose run web python manage.py loaddata order/fixtures/status`  
`sudo docker-compose run web python manage.py loaddata catalog/fixtures/product`

## Tests

`sudo docker-compose run web python manage.py test`
