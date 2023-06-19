import pandas as pd
import sqlite3

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator

CON = sqlite3.connect('example.db')

# Повторим предыдущий код с небольшим измененеием, теперь файлы 
# записываются на диск, а не передаются в потоке исполнения

def extract_data(url, tmp_file, **context):
    """ Extract CSV
    """
    pd.read_csv(url).to_csv(tmp_file) # Изменение to_csv


def transform_data(group, agreg, tmp_file, tmp_agg_file, **context):
    """ Group by data
    """
    data = pd.read_csv(tmp_file) # Изменение read_csv
    data.groupby(group).agg(agreg).reset_index().to_csv(tmp_agg_file) # Изменение to_csv
 

def load_data(tmp_file, table_name, conn=CON, **context):
    """ Load to DB
    """
    data = pd.read_csv(tmp_file)# Изменение read_csv
    data["insert_time"] = pd.to_datetime("now")
    data.to_sql(table_name, conn, if_exists='replace', index=False)




# Создаем DAG(контейнер) в который поместим наши задачи
# Для DAG-а характерны следующие атрибуты
# - Интервал запусков
# - Начальная точка запуска
with DAG(dag_id='dag',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily', # Интервал запусков
         start_date=days_ago(1) # Начальная точка запуска
    ) as dag:

 
    # Создадим задачу которая будет запускать питон функция
    # Все именно так, создаем код для запуска другого кода
    extract_data = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/dm-novikov/stepik_airflow_course/main/data/data.csv',
            'tmp_file': '/tmp/file.csv'}
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'tmp_agg_file': '/tmp/file_agg.csv',
            'group': ['A', 'B', 'C'],
            'agreg': {"D": sum}}
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={
            'tmp_file': '/tmp/file_agg.csv',
            'table_name': 'table'
        }
    )

    # Создадим задачу которая будет отправлять файл на почту
    email_op = EmailOperator(
        task_id='send_email',
        to="gendulum@yandex.ru",
        subject="Test Email Please Ignore",
        html_content=None,
        files=['/tmp/file_agg.csv']
    )

    # Создадим порядок выполнения задач
    # В данном случае 2 задачи буудт последователньы и ещё 2 парараллельны
    extract_data >> transform_data >> [load_data, email_op]