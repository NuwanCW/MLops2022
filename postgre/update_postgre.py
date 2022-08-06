import json
import os

import pandas as pd
import psycopg2
from redis_om import get_redis_connection

redis_db = get_redis_connection(host="192.168.1.136", port="6379")


def read_redis_data(key="pred_data", start=0, end=-1):
    data = redis_db.lrange(key, start, end)
    redis_db.delete(key)
    return data


def process_data():
    data = read_redis_data()
    if data:
        records_list = []
        for rec in data:
            record = json.loads(rec)
            if record["response"]["status-code"] == 200:
                for i, pred in enumerate(record["response"]["data"]["predictions"]):
                    record_to_postgre = {
                        "redis_id": record["id"] + "_" + str(i),
                        "redis_time_val": record["time"],
                        "redis_input_text": pred["input_text"],
                        "redis_predicted_tag": pred["predicted_tag"],
                    }

                    records_list.append(record_to_postgre)
        return pd.DataFrame(records_list)
    return pd.DataFrame()


def update_table(table="predictions"):
    conn = None

    # connect to the PostgreSQL server
    conn = psycopg2.connect(
        database="postgres", user="postgres", password="postgres", host="192.168.1.136", port="5834"
    )
    df = process_data()
    if len(df) > 0:
        df.to_csv("./tmp_df.csv", index=False, header=False)
        f = open("./tmp_df.csv")
        # create a cursor
        cursor = conn.cursor()
        print("Opened database successfully")
        try:
            cursor.copy_from(f, table, sep=",")
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            os.remove("./tmp_df.csv")
            print(f"Error: {error}")
            conn.rollback()
            cursor.close()
            return 1
        print("copy form file done")
        cursor.close()
        os.remove("./tmp_df.csv")
    else:
        print("all uptodate")


update_table()
# print(read_redis_data())
