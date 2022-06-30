import os
import json
import mysql.connector
import time



insert_new_message = "INSERT INTO chat (username, message) VALUES (%s, %s);"
get_messages_sql = 'SELECT * from chat ORDER BY cid ASC;'

actions = ['get_messages', 'send_message']




def re(data):
    return {
        'statusCode': 200,
        'body': json.dumps(str(data))
    }


def lambda_handler(event, context):
    time.sleep(3)
    # TODO implement
    # print(dir(event))
    action = 'get_messages'
    print(os.environ['RDS_DB_NAME'])
    action = str(event.get('headers').get('action'))
    if action == 'None':
        return re('Unable to complete request.')

    if len(list(filter(lambda x: x == action, actions))) < 1:
        return re('Unable to complete request: Unknown action. makine soguk')

    # return controller(event,action)
    if action == 'get_messages':
        cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], passwd=os.environ['RDS_PASSWORD'],
                                      database=os.environ['RDS_DB_NAME'], port=os.environ['RDS_PORT'], charset='utf8')
        cur = cnx.cursor()
        cur.execute(get_messages_sql)
        res = cur.fetchall()

        cnx.close()
        ret = []
        for row in res:
            ret.append({"cid": row[0], "username": row[1], "message": row[2], "time": row[3]})

        return {'statusCode': 200, 'body': json.dumps(ret, indent=0, sort_keys=True, default=str)}
    if action == 'send_message':
        username = str(event.get('headers').get('username'))
        message = str(event.get('headers').get('message'))
        cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], passwd=os.environ['RDS_PASSWORD'],
                                      database=os.environ['RDS_DB_NAME'], port=os.environ['RDS_PORT'], charset='utf8')
        cur = cnx.cursor()
        cur.execute(insert_new_message, (username, message))
        cnx.commit()
        cnx.close()
        return {'statusCode': 200, 'body': json.dumps(cur.lastrowid, indent=0, sort_keys=True, default=str)}