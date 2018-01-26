import socket
import sys
import time
import json
import requests

READ_TIMEOUT=20

def write_metric(carbon_server, mPath, metrics, CARBON_PORT=2003):
    '''
    get metrics and send it to graphite
    ex: [{'target': 'sumSeries(metric.path.*)', 'datapoints': [[20.0, 1516966190], [20.0, 1516966200], [20.0, 1516966210], [20.0, 1516966220], [20.0, 1516966230], [20.0, 1516966240], [20.0, 1516966250], [20.0, 1516966260], [20.0, 1516966270], [None, 1516966280]]}]
    '''
    message = ''
    for metric in metrics[0]["datapoints"]:
      if metric[0]:
        # print('writing metric:{} to ds:{}. v:{} ts:{}'.format(mPath, carbon_server, metric[0], metric[1]))
        message += '{} {} {}'.format(mPath, metric[0], metric[1]) + '\n'
    print(len(message))
    message = bytes(message, 'utf-8')
    sock = socket.socket()
    sock.settimeout(10)
    try:
        sock.connect((carbon_server, CARBON_PORT))
    except:
        print('{} Could not send metrics to {}:{}'.format(DC, carbon_server, CARBON_PORT))
        return False

    sock.sendall(message)
    sock.close()
    return True


def read_metric(graphite_web, target, fromDelta=1800, untilDelta=0):
  ts = time.time()
  tsfrom = int(ts - fromDelta)
  tsuntil = int(ts - untilDelta)
  url = 'https://{}/render/?target={}&format=json&from={}&until={}'.format(graphite_web, target, tsfrom, tsuntil)
  print(url)
  req = requests.get(url, timeout=READ_TIMEOUT)
  data_list = req.json()
  return data_list


def scrap_metric(event, context):
  ds = event["ds"]
  tsdb = event["tsdb"] # storage
  target = event["target"]
  result_path = event["result_path"]
  timestamp = int(time.time())
  metrics = read_metric(ds, target)
  # print(metrics)
  if len(metrics) > 1:
    return False
  
  return write_metric(tsdb, result_path, metrics)
  

if __name__ == '__main__':
  event = json.load(open('data.json'))
  res = scrap_metric(event, "")
  print(res)
