# Orchestrating dbt with Prefect

In this tutorial, we will explore how we can use Prefect to orchestrate dbt jobs. The purpose is to make it run on Kubernetes supplied by Docker Desktop so that it can easily be reproduced. 

For demo purposes, we needed a simple dbt project running on PostgreSQL. Instead of creating one from scratch, we used a clone of the repository from [this tutorial](ttps://www.startdataengineering.com/post/dbt-data-build-tool-tutorial/). To be more precise, we reused the files from [this commit](https://github.com/josephmachado/simple_dbt_project/tree/392097b2758b221333445f860383ea59fd18b7e8), but instead of making a direct clone, we reorganised it a little bit. 

## Prerequisites

To go through this tutorial, you will need: 

    - Docker
    - docker-compose
    - dbt
    - pgcli
    - git 
    - Prefect

### Setup PostgreSQL database for the demo

We will start a PostgreSQL container and load the source data for our demo using docker-compose: 

```
cd warehouse-setup && docker-compose up -d

```

In a real-life scenario, the warehouse is typically a cloud data warehouse such as Snowflake or BigQuery and source data is loading using tools such as Fivetran or Airbyte. 

When the necessary resources are created, you can verify that the database container is created and the data is loaded by connecting to it using `pgcli`: 

```
pgcli -h localhost -U dbt -p 5432 -d dbt
```

When running the command, you will be prompted for the password. 

## Dockerfile

We will create a Docker image containing both dbt, Prefect and our flow and dbt code. This can be done by running the following command: 

```
docker build -t prefect-dbt-demo:latest .
```

The Dockerfile might look complicated at first, but it is constructed in such a way that: 

    - all dependencies (including `dbt deps`) are already installed
    - a container using this image can be run as non-root user

To run a shell in a new container with this image, execute 

```
docker run -it --entrypoint bash prefect-dbt-demo:latest
```


## Prefect flow

TO DO

## Clean up of resources 

To clean up the PostgreSQL container, run 

```
cd warehouse-setup && docker compose down
```