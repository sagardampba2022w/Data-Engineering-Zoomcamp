
# Initialising pg db

docker run -it \
  -e  POSTGRES_USER="root" \
  -e  POSTGRES_PASSWORD="root" \
  -e  POSTGRES_DB="ny_taxi" \
  -v  $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

# Testing db
pgcli -h localhost -p 5432 -U root -d ny_taxi

#use password as root


# running pg admin console

docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="admin" \
  -p 8080:80 \
  dpage/pgadmin4


# Creating network between pg database and pg admin
docker network create pg-network


docker run -it \
  -e  POSTGRES_USER="root" \
  -e  POSTGRES_PASSWORD="root" \
  -e  POSTGRES_DB="ny_taxi" \
  -v  $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network pg-network \
  --name pg-database \
  postgres:13


  
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="admin" \
  -p 8080:80 \
  --network pg-network \
  --name pgadmin \
  dpage/pgadmin4

# for chunking and ingesting in db

  python ingest_data_parquet.py \
  --user root \
  --password root \
  --host localhost \
  --port 5432 \
  --db ny_taxi \
  --table_name yellow_taxi_data \
  --url https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet


  docker build -t taxi_ingest:v001 .

docker run taxi_ingest:v001 \
  --user root \
  --password root \
  --host localhost \
  --port 5432 \
  --db ny_taxi \
  --table_name yellow_taxi_data \
  --url https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet