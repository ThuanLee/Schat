# chat_real_time

### Note: recommend to use python 3.10 or above

## Setup & Installation

Make sure you have the latest version of Python installed (recommend 3.10 and above).

```bash
git clone <repo-url>
```

Create virtual environment (optional)

```bash
virtualenv venv
```

```bash
source ./venv/Scripts/active (windows)
source ./venv/bin/active (MacOS/Linux)
```

Install necessary dependencies

```bash
pip install -r requirements.txt
```
#### !Attention: some dependencies such as mysqlclient will require other conditions

## Configure file .env

- Copy file .env.sample to file .env

- Fill in the appropriate values for the variables

## Running The App

Run command below to run server on port 8000
```bash
python manage.py runserver 0.0.0.0:8000
```

## Viewing The App

Go to `http://127.0.0.1:8000`

![image](https://github.com/ThuanLee/Schat/assets/100220743/fe533670-9176-4f0a-adb1-fc855ce5c7f9)

## Using docker to run

Make sure you install `docker` and `docker-compose` with version from v2:

Run command to build image and container:
```bash
docker-compose up
```

If you have some chances in requirements.txt or something like that, you can build container again by using command:
```bash
docker-compose up --build
```

If you want to access to docker container in docker-compose to use some other commands such as: migrate, ...:
```bash
docker-compose exec <name container> sh
```

## Database

![image](https://github.com/ThuanLee/Schat/assets/100220743/b6e261a2-7099-48f7-aed6-cad8a5c287aa)

