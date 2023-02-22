# dinopedia
# Super user
admin
victorcidfiguera@gmail.com
Abc123,666

## Prerequisites
Before running the application, you will need to have the following software installed on your machine:

Docker[https://docs.docker.com/install/]
Docker Compose[https://docs.docker.com/compose/install/]

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
docker-compose build
```

4. Apply the database migrations:

```bash
docker-compose run web python manage.py migrate
```

5. Start the application:

```bash
docker-compose up
```


This will start the two services defined in the `docker-compose.yml` file (db and web) and the Django server should be accessible at `http://localhost:8000`.

Note that the first time you run the `docker-compose up` command, it will take a few minutes to build the Docker image for the web service, but subsequent runs will be much faster.

If you make changes to your models in `models.py` or add new dependencies to your `requirements.txt` file, you will need to rebuild the Docker image for the `web` service by running the `docker-compose build` command again.

To stop the application, press `Ctrl+C` in the terminal where `docker-compose` up is running.

That's it! With these steps, you should have the Dinopedia application running on your machine.