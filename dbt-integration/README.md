# Orchestrating dbt with Prefect

[Intro text here]

Reference https://www.startdataengineering.com/post/dbt-data-build-tool-tutorial/

## Prerequisites

To go through this tutorial, you will need: 

    - Docker
    - docker-compose
    - dbt
    - pgcli
    - git 
    - Prefect

### Setup PostgreSQL database for the demo

To start a PostgreSQL container and load the source data for our demo, run: 

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

## Prefect flow

## Clean up of resources 

To clean up the PostgreSQL container, run 

```
cd warehouse-setup && docker compose down
```