# D - Commerce

D-Commmerce is an experimental web application for creating an online marketplace. It is not intended for real-world use and does not support actual buying or selling of products. Users can sign up, buy and sell products, manage stock and delivering and more. It is built with Django, Bootstrap, Postgres and Docker.

### Requirements
- Docker
- Docker-Compose
- Make (optional)
#### Installation
1.  Clone the repositoy: `git clone https://github.com/urielmayo/d_commerce.git (http)` or `git clone git@github.com:urielmayo/d_commerce.git (ssh)`
2. Create an `.env` file in the root project directory with the following variables :
```
POSTGRES_DB=postgres_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_password

SECRET_KEY=your_secret_key
POSTGRES_NAME=postgres_name
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
3. Build the containers: `docker-compose build`
4. Create the migrations: `docker-compose run --rm --service-ports web python manage.py makemigrations`
5. Create a superuser: `docker-compose run --rm --service-ports web python manage.py createsuperuser`
6. Run the containers: `docker-compose up -d`
7. Search in your browser: `http://localhost:8000`

> You can also use the commands `make migrations` and `make run` for steps 6 and 7. Install make for that

You are done! No you can enjoy the app.