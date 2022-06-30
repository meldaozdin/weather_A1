import os
import json
import mysql.connector
import time


get_data = 'SELECT * from weather ORDER BY id ASC;'


def lambda_handler(event, context):
    cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], passwd=os.environ['RDS_PASSWORD'],
                                  database=os.environ['RDS_DB_NAME'], port=os.environ['RDS_PORT'], charset='utf8')
    cur = cnx.cursor()
    cur.execute(get_data)
    res = cur.fetchall()

    cnx.close()
    ret = []
    for row in res:
        ret.append({"id": row[0], "max_temp": row[1], "min_temp": row[2], "avg_temp": row[3], "date": row[4]})
    return {'statusCode': 200,'headers': {"content-type": "application/json"}, 'body': json.dumps(ret, indent=0, sort_keys=True, default=str)}
    # return controller(event,action)
