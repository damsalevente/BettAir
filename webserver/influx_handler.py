from datetime import datetime

from influxdb_client import Point, InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

"""
Configure credentials BIG TODO into ENV FILE
"""
influx_cloud_url = "https://us-central1-1.gcp.cloud2.influxdata.com"
influx_cloud_token = "trjNGVUUlH-kWgP8zyEXHGxCMGV5749Mzh5ccYNPzP93Kk1VUmXCXvqhnb7vMhPdHoQApE9IyNUJBigS94OSFQ=="
bucket = 'mybucket'
org = '18d7dd6618fbcd6d'



def send_data(what, value):
    """ 
    this function sends the data as json, and checks if it was succesfull 
    """
    client = InfluxDBClient(url=influx_cloud_url, token=influx_cloud_token)
    try:
        point = Point("measurement").field(what,value).time(time=datetime.utcnow())

        # if data is incorrect, don't send anything
        if point is None:
            return -1

        """
        Write data by Point structure
        """

        print(f'Writing to InfluxDB cloud: {point.to_line_protocol()} ...')

        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)

        print()
        print('success')
        print()
        print()


    except Exception as e:
        print(e)
    finally:
        client.close()

if __name__ == "__main__":

    send_data({"kind":"temparature", "key":"CAT", "value":0})
    send_data({"kind":"co2", "key":"CAT", "value":1})
    send_data({"kind":"tvoc", "key":"CAT", "value":5})
    send_data({"kind":"co2", "key":"CAT", "value":8})
    send_data({"kind":"light", "key":"CAT", "value":600})

    send_data({"kind":"temparature", "key":"CAT", "value":0})
    send_data({"kind":"co2", "key":"CAT", "value":1})
    send_data({"kind":"tvoc", "key":"CAT", "value":5})
    send_data({"kind":"co2", "key":"CAT", "value":8})
    send_data({"kind":"light", "key":"CAT", "value":600})

    send_data({"kind":"temparature", "key":"CAT", "value":0})
    send_data({"kind":"co2", "key":"CAT", "value":1})
    send_data({"kind":"tvoc", "key":"CAT", "value":5})
    send_data({"kind":"co2", "key":"CAT", "value":8})
    send_data({"kind":"light", "key":"CAT", "value":600})
    send_data({"kind":"temparature", "key":"CAT", "value":0})
    send_data({"kind":"co2", "key":"CAT", "value":1})
    send_data({"kind":"tvoc", "key":"CAT", "value":5})
    send_data({"kind":"co2", "key":"CAT", "value":8})
    send_data({"kind":"light", "key":"CAT", "value":600})
