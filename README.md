# dinopedia
# Super user
- User: dino-admin
- Password: Dinopedia-admin,123

## Prerequisites
Before running the application, you will need to have the following software installed on your machine:

* [Docker](https://docs.docker.com/install/)
* [Docker Compose plug in](https://docs.docker.com/compose/install/)

## Installation
To install and run the application, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/<your-username>/dinopedia.git
```

2. Navigate to the project directory:

```bash
cd dinopedia
```

3. Build the Docker image for the web service:

```bash
docker-compose up
```


This will start the two services defined in the `docker-compose.yml` file (db and web) and the Django server should be accessible at `http://localhost:8000`.

Note that the first time you run the `docker-compose up` command, it will take a few minutes to build the Docker image for the web service, but subsequent runs will be much faster.

If you make changes to your models in `models.py` or add new dependencies to your `requirements.txt` file, you will need to rebuild the Docker image for the `web` service by running the `docker-compose build` command again.

To stop the application, press `Ctrl+C` in the terminal where `docker-compose` up is running.

That's it! With these steps, you should have the Dinopedia application running on your machine.

## Cleaning up
To stop the application, press `Ctrl+C` in the terminal where `docker-compose` up is running.

To remove the Docker containers and volumes, run the following command:

**Please be careful with this command, it will remove all your containers and volumes.**

`docker network prune -f && docker volume prune -f && docker container prune -f && docker image prune --all -f`

Happy coding!

# Learn how to integrate PlanetScale with a sample Django application

This sample application demonstrates how to connect to a PlanetScale MySQL database, create and run migrations, seed the database, and display the data.

For the full tutorial, see the [Django PlanetScale documentation](https://planetscale.com/docs/tutorials/connect-django-app).

## Set up the Django app

1. Clone the starter Django application:

```bash
git clone git@github.com:planetscale/django-example.git
cd django-example
```

2. Start the virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

For Windows, use `env/Scripts/activate`.

3. Install the required packages:

```bash
pip install -r ./requirements.txt
```

## Set up the database

1. Sign up for a [free PlanetScale account](https://planetscale.com/sign-up) and create a new database.

2. Click the "**Connect**" button to generate credentials for database branch (`main` is default). Select "**Django**" from the language dropdown and copy the values in the sample `.env` file.

3. Modify your `.env` file in your Django app with the values from the previous step:

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
MYSQL_ATTR_SSL_CA=
```

> **Note**: The value for `MYSQL_ATTR_SSL_CA` may differ [depending on your operating system](https://planetscale.com/docs/reference/secure-connections#ca-root-configuration).

4. In the `mysite/settings.py` file, scroll down and look for the `DATABASES` object. Replace it with the following:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_psdb_engine',
        'NAME': os.environ.get('DB_NAME'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'OPTIONS': {'ssl': {'ca': os.environ.get('MYSQL_ATTR_SSL_CA')}}
    }
}
```

## Run migrations and seeder

1. Change directory and run the migrations and seeder with:

```bash
cd mysite/
python3 manage.py migrate
```

## Start the application

1. Start the server with:

```bash
python3 manage.py runserver
```

2. Navigate to [`localhost:8000/products`](http://localhost:8000/products) to see a list of data from the products table. 
