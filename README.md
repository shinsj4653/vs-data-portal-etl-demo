# VISANG DataPortal ETL-demo
> 비상교육 데이터 포털의 DB 중앙 관리 시스템을 위한 `Apache Airflow ETL 구축` 실습  

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/a0644525-93cf-4d7a-8229-6b2843ee4f15)

*Demo ETL 파이프라인 구축 성공*

## Apache Airflow

시작에 앞서, `Apache Airflow`란 무엇인지 알아보고 가자.

- 개념 - [Airflow 엄청 자세한 튜토리얼](https://velog.io/@clueless_coder/Airflow-%EC%97%84%EC%B2%AD-%EC%9E%90%EC%84%B8%ED%95%9C-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC-%EC%99%95%EC%B4%88%EC%8B%AC%EC%9E%90%EC%9A%A9#%E2%99%80%EF%B8%8F-%EB%8C%80%EA%B7%B8-%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0-%EC%97%90%EB%9F%AC-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0)

- 장단점 - [Airflow 장단점](https://velog.io/@sophi_e/Airflow-%EA%B8%B0%EC%B4%88-%EA%B0%9C%EB%85%90-%EB%B0%8F-%EC%9E%A5%EB%8B%A8%EC%A0%90)

## Docker Compose

- 개념 - [12장. Docker-Compose](https://velog.io/@ckstn0777/12%EC%9E%A5.-Docker-Compose)

- 명령어 - [Docker Compose 커맨드 사용법](https://www.daleseo.com/docker-compose/)

## Windows 내에 Ubuntu 사용을 위한 WSL 구성

Docker Desktop 설치 후, 실행하려고 하는데 다음과 같은 에러 발생  
![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/4ed2d24e-cad2-4cc9-b13b-864ac57f51ec)  
*Error : Docker Desktop requires a newer WSL kernel version*


[Docker Desktop requires a newer WSL kernel version.](https://park-duck.tistory.com/entry/Docker-wsl-%EB%AC%B4%ED%95%9C%EB%8C%80%EA%B8%B0-feat-Docker-Desktop-requires-a-newer-WSL-kernel-version)

다음과 같이 해결해주면 된다.

1. Windows PowerShell 관리자 권한 실행  

2. 리눅스 서브 시스템 활성화
```bash
$ dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```  
3. 가상 머신 플랫폼 활성화
```bash
$ dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
4. Linux 커널 업데이트

https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi  
윗 링크를 통해 .msi 다운로드

5. WSL 2를 default로 설정
```bash
$ wsl --set-default-version 2
```


## Fetching docker-compose.yml & Run Docker-Compose 

Airflow를 Docker Compose를 사용하여 배포하기 위해, docker-compose.yml 을 가져와서 실행해준다.
```bash
$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.7.2/docker-compose.yaml'
```
나 같은 경우, `VSCode 내의 Bash 터미널`을 사용하였다.

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/2e1ed1eb-e23b-40c0-8f11-c7a4eeda0e71)
*bash 터미널을 활용하여 yaml 파일 가져와서 설치*

### docker-compose.yml & config 초기 설정

1. example dag 파일들 삭제

예시 dag 파일들이 있지만, 너무 양이 많은 관계로 삭제해줬다.

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/10ebe265-c44c-4267-ab5d-f3e698876650)  
*docker-compose.yml 수정1*


2. timezone 수정

한국 시간대로 맞추기 위해 다음 옵션을 추가

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/5b2aa345-aae0-400e-8473-43fa31dd0bdc)  

*docker-compose.yml 수정 2*

3. airflow.cfg 수정

cfg 파일을 밖에서 원활하게 수정하기 위해 위에서 airflow.cfg 파일을 마운트하기로 하였다.  

시스템 내부의 오리지널 cfg 파일은 `/opt/airflow/airflow.cfg` 에 위치하고 있으며, 이를 복사하여 로컬 환경 내의 config 폴더 안에 넣어줬다.  

그 다음, airflow.cfg 파일 내의 default_timezone 값을 `Asia/Seoul` 로 수정하였다.

```python
# Default timezone in case supplied date times are naive
# can be utc (default), system, or any IANA timezone string (e.g. Europe/Amsterdam)
#
# Variable: AIRFLOW__CORE__DEFAULT_TIMEZONE
#
default_timezone = Asia/Seoul
```
### Initializing Environment
 
에어플로우 개발 전 환경 구성과 유저 권한을 세팅해야함  

1. 에어플로우 유저 권한 세팅
```bash
$ mkdir -p ./dags ./logs ./plugins # mkdir -p 옵션 : 여러 하위 디렉토리를 생성시에 사용
```
그 다음, .env 폴더 생성 후 다음 코드 입력  

```bash
AIRFLOW_UID=50000
```

(참고) [docker compose 지원 환경변수](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#docker-compose-env-variables)


2. 에어플로우 DB 초기화
```bash
$ docker-compose up airflow-init
```

3. 나머지 이미지들도 전부 실행
```bash
$ docker compose up -d
```


4. 마지막으로 flower를 실행시켜준다.
```bash
$ docker compose up -d flower
```


## `sqlalchemy` 기반 DAG 파일 생성
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine
import pandas as pd

# Define your default_args, schedule_interval, and other DAG configurations
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 24),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'pionada_etl',
    default_args=default_args,
    description='An example DAG to copy data from one PostgreSQL DB to another',
    schedule_interval=timedelta(days=1),  # Set your schedule interval
)

# Define a function to fetch data from source PostgreSQL DB
def fetch_data_from_source_db():
    source_engine = create_engine(f'postgresql://{FETCH_USER_NAME}:{FETCH_USER_PW}@{FETCH_DB_URL}/{FETCH_DB_NAME}')
    df = pd.read_sql(f'SELECT * FROM {FETCH_TABLE_NAME}', source_engine)
    return df

# Define a function to write data to target PostgreSQL DB
def write_data_to_target_db(**kwargs):
    target_engine = create_engine(f'postgresql://{WRITE_USER_NAME}:{WRITE_USER_PW}@{WRITE_DB_URL}/{WRITE_DB_NAME}')
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='fetch_data_from_source_db')
    df.to_sql(f'{WRITE_TABLE_NAME}', target_engine, if_exists='replace', index=False)

# Define tasks
fetch_data_task = PythonOperator(
    task_id='fetch_data_from_source_db',
    python_callable=fetch_data_from_source_db,
    dag=dag,
)

write_data_task = PythonOperator(
    task_id='write_data_to_target_db',
    python_callable=write_data_to_target_db,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
fetch_data_task >> write_data_task
```
회사 내 원하는 서비스의 DB정보를 가져와주는 `fetch_data_task` 와 가져온 데이터를 Airflow 내의 PostgreSQL 안에 적재시켜주는 `write_data_task` 를 정의하는 DAG 파일을 생성해줬다.  

`sqlalchemy` 를 통한 DB 연결 및 SQL 문 실행을 수행하였고, `xcom_pull` 을 통해 task 사이에서의 데이터 전달이 가능해지도록 구현하였다. 

`PythonOperator` 사용 시, return이 자동으로 Xcom 변수로 지정되게 된다. 또한, `provide_context` 를 통해 Task Instance의 시행 일자, Task ID와 같은 부가 정보들도 액세스 가능해진다.

작성 완료 후, `dag` 폴더 내에 넣어주고 나서 새로고침하면 바로 웹 상에서 확인 가능하다.

## Apache WebServer

1. 디폴트 계정으로 로그인


아이디 : airflow, 비번 : airflow

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/0bd7b658-4218-49cd-8c58-82d7e453077a)  


*웹 서버 첫 화면*  

메인 화면에서 부터 `KST 타임 설정`이 잘 된 것을 확인할 수 있다.



2. 현재 DAG 파일들 상태 확인

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/76874885-4450-475c-9b8d-8fe9914e1c5b)

*DAGs 메뉴 화면*  

원하는 DAG 을 선택한 후, 실행되는 과정을 상세하게 확인할 수 있다.



3. Success, 혹은 Failed 이유를 로그를 통해 확인 가능

![image](https://github.com/shinsj4653/vs-data-portal-etl-demo/assets/49470452/f251c091-db49-4069-abc0-41713bebf491)
*Total success, 혹은 Total failed 클릭 시 상세 로그 확인 가능*

로그 확인을 통해 DAG의 Task 중, `create_engine` 내에 들어가는 url 형식이 잘못된 것을 확인하였고 이를 수정하고 난 후 성공적으로 `Airflow 기반 ETL 파이프라인을 구축`할 수 있었다.


Total success, 혹은 Total failed 클릭 시 상세 로그 확인 가능

로그 확인을 통해 DAG의 Task 중, create_engine 내에 들어가는 url 형식이 잘못된 것을 확인하였고 이를 수정하고 난 후 성공적으로 Airflow 기반 ETL 파이프라인을 구축할 수 있었다.
