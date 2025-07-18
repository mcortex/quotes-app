# Quotes-App

## API Backend

This is an API built in Python with FastAPI + SQLModel and its corresponding MySQL database.

## Frontend SPA

This is a Frontend Single Page Application built with VUE, Axios and Vite.

## How to run using Docker only

This is a local docker alternative to run the app, you may lose the high availability that Kubernetes provides.

### Start the Database

```bash
docker run --name quotes-mysql -p 33306:3306/tcp -v $(pwd)/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD='Password123*' -d mysql:9.3.0
```

### Get the container IP (DB_IP)

```bash
docker inspect quotes-mysql |grep IPAddress | grep -v Secondary | tail -1
```

### Start the API

```bash
cd backend

docker build -t quotes-api:v0.0.1 .

docker run --name quotes-api -e DB_HOST=<DB_IP> -e DB_PORT=3306 -e DB_USER=root -e DB_PASS='Password123*' -p 8000:8000 quotes-api:v0.0.1
```

### Get the container IP (API_IP)

```bash
docker inspect quotes-api |grep IPAddress | grep -v Secondary | tail -1
```

### Start the frontend

```bash
cd frontend

docker build -t quotes-frontend:v0.0.1 .

docker run --name quotes-frontend -e VITE_API_URL='http://<API_IP>:8000' -p 80:80 quotes-frontend:v0.0.1
```

### Query the API

```bash
# View quotes
curl -X GET 127.0.0.1:8000/quotes/all -s | jq

# Check API Docs (from browser)
http://127.0.0.1:8000/docs
```

### Access the frontend

```bash
sudo echo "127.0.0.1 quotes.local" >> /etc/hosts

# in browser: http://quotes.local
```