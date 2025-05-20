#!/bin/bash
clear

# create private network
docker network create lvp-networks

sudo docker compose down
sudo docker compose up --build -d




