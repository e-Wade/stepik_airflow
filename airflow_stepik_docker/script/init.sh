#!/bin/bash

# Создание БД
sleep 10
airflow upgradedb
sleep 10

# Создание пользователя
airflow users create \
          --username admin \
          --firstname admin \
          --lastname admin \
          --role Admin \
          --email admin@example.org \
          -p 12345

# Запуск шедулера и вебсервера
airflow webserver & airflow scheduler
