# Simpsons Quotes API

Se tiene una API hecha en Python con FastApi+SQLAlchemy y su correspondiente Base de datos en MySQL.

Al momento la misma se encuentra dockerizada y se puede ejecutar localmente:

## Como ejecutar utilizando solo Docker:

### Levantar la Base de Datos:

```bash
# Ejecutamos la base con una persistencia
cd db

docker run --name simpsons-mysql -p 33306:3306/tcp -v $(pwd)/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=Password123 -d mysql:8.0.29
```

### Obtenemos la ip del container (IP_BD)

```bash
docker inspect simpsons-mysql |grep IPAddress
```

### Cargamos los datos:

```bash
mysql -P3306 -h <IP_BD>-u root -p < alta_db.sql
```

### Levantar la API:

```bash
cd api

docker build -t simpsons-quotes:0.1.3 .

docker run --name simpsons-api -e DB_HOST=<IP_BD> -e DB_PORT=3306 -e DB_USER=root -e DB_PASS=Password123 simpsons-quotes:0.1.3
```

### Consultar a la API:

```bash
# Ver frases
curl "http://172.17.0.3:8000/quotes" -s

# Consultar API Docs (desde el navegador)
http://172.17.0.3:8000/docs
```

![homer-console](images/homer-simpson.gif)
