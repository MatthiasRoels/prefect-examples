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

To start a PostgreSQL container and 

```
cd warehouse-setup && docker-compose up -d

```

```
pgcli -h localhost -U dbt -p 5432 -d dbt
```

## Dockerfile 

## Prefect flow