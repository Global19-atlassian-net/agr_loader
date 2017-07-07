[![Build Status](https://travis-ci.org/alliance-genome/agr_loader.svg?branch=master)](https://travis-ci.org/alliance-genome/agr_loader)


# Alliance of Genome Resources Loader
An initial loader prototype for the web portal of the Alliance of Genome
Resources.

## Requirements
- Docker
- Docker-compose (can be installed via `pip`: `pip install docker-compose`).

## Installation
- Build the local image with `make build`.
- Start the Neo4j database with `make startdb`. Allow ~10 seconds for Neo4j to initialize.

## Running the Loader
- Run the loader with `make run`.

## Accessing the Neo4j shell
From your command line: `docker exec --interactive neo4j_nqa bin/neo4j-shell -path /db/data`

## Stopping and Removing the Database
- Once finished, stop the database with `make stopdb`.
- Optionally, remove the database with `make removedb`.
