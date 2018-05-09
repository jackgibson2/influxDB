#!/usr/bin/python

import argparse
import csv
import string
import random
from influxdb import InfluxDBClient
from datetime import datetime  
from datetime import timedelta  


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--customers', type=int, default=10, help='Random customers to generate')
parser.add_argument('-m', '--minutes', type=int, default=120, help='Number of minutes before datetime.now() to start loading data from')
parser.add_argument('-t', '--transactions', type=int, default=100, help='Maximum possible number of transactions to load per customer per time interval')
parser.add_argument('-i', '--increment', type=int, default=5, help='Time interval to increment from starting time')
args = parser.parse_args()


client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
client.drop_database('example')
