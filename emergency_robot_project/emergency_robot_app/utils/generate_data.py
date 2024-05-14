import pandas as pd
import random
from datetime import datetime
import psycopg2

def generate_earthquake_victims_dataframe(num_victims:int) -> pd.DataFrame:
    istanbul_latitude = 41.0422
    istanbul_longitude = 29.0097
    max_distance = 0.05  

    data = []
    for _ in range(num_victims):
        person_id = f"Person_{random.randint(1, 1000)}"
        latitude = round(random.uniform(istanbul_latitude - max_distance, istanbul_latitude + max_distance), 6)
        longitude = round(random.uniform(istanbul_longitude - max_distance, istanbul_longitude + max_distance), 6)
        timestamp = datetime.now()
        status = random.choice(['Dead', 'No Injury', 'Minor Injury', 'Major Injury'])
        source = random.choice(['Camera', 'Microphone', 'PIR Sensor'])

        data.append((person_id, latitude, longitude, timestamp, status, source))

    columns = ['person_id', 'latitude', 'longitude', 'timestamp', 'status', 'source']
    df = pd.DataFrame(data, columns=columns)
    return df

def insert_dataframe_to_postgresql(df:pd.DataFrame, table_name:str):
    conn = psycopg2.connect(
        dbname="EMERGENCY_ROBOT_DB",
        user="postgres",
        password="egemen123",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute(f"TRUNCATE TABLE {table_name};")
    for _, row in df.iterrows():
        cur.execute(f"INSERT INTO {table_name} (person_id, latitude, longitude, timestamp, status, source) VALUES (%s, %s, %s, %s, %s, %s);", row)

    conn.commit()
    cur.close()
    conn.close()

df = generate_earthquake_victims_dataframe(10) 
insert_dataframe_to_postgresql(df, "earthquake_victims")