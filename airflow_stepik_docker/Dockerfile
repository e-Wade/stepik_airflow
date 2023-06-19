# Возьмем за основу образ 
FROM python:3.7

# Airflow глобальные переменные
ARG AIRFLOW_VERSION=1.10.14 # В прошлых работах мы использовали 2.0 версию, но на этом уроке поработаем с предыдущей версией
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Сборка airflow
RUN pip install apache-airflow[postgres]==${AIRFLOW_VERSION} \
    pip install SQLAlchemy==1.3.23 \
    pip install markupsafe==2.0.1 \
    pip install wtforms==2.3.3 \
    pip install flask-bcrypt

# Создаем директрию для скриптов
# RUN mkdir /project
WORKDIR ${AIRFLOW_USER_HOME}


# Копируем скрипты и конфиг файл
COPY script/ ${AIRFLOW_USER_HOME}/scripts/
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Доступы для скрипта
RUN chmod +x ./scripts/init.sh
# RUN chmod +x ./scripts/create_user.py

# Запускаем sh скрипт
ENTRYPOINT ["./scripts/init.sh"]
# CMD ["python3", "./scripts/create_user.py"]
