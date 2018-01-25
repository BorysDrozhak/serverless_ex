import socket
import sys
import time
import json
import requests

READ_TIMEOUT=10

def write_metric(carbon_server, mPath, mValue, timestamp, CARBON_PORT=2003):
    message = '{} {} {}'.format(mPath, mValue, timestamp) + '\n'
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


def read_metric(graphite_web, target, fromDelta=100, untilDelta=0):
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
  result = read_metric(ds, target)

  if len(result) > 1:
    return False

  for metric in result[0]["datapoints"]:
    if metric[0]:
      print('writing metric:{} to ds:{}. v:{} ts:{}'.format(result_path, ds, metric[0], metric[1]))
      write_metric(tsdb, result_path, metric[0], metric[1])
  return True


if __name__ == '__main__':
  event = json.load(open('data.json'))
  res = scrap_metric(event, "")
  print(res)
