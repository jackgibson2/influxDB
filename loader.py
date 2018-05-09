#!/usr/bin/python

import argparse
import csv
import string
import random
from influxdb import InfluxDBClient
from datetime import datetime  
from datetime import timedelta  

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for x in range(size))

def build_json(measurement,customer, country, method, stp, currency, amount, time):
    jsonString = [
        {
            'measurement' : measurement, 
            'tags' : {
                'customer' : customer,
                'country' : country,
                'method' : method,
                'stp' : stp,
                'currency' : currency
            },
            'time' : time,
            'fields' : {
                'amount' : amount
            }
        }  
    ]
    return jsonString


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--customers', type=int, default=10, help='Random customers to generate')
parser.add_argument('-m', '--minutes', type=int, default=120, help='Number of minutes before datetime.now() to start loading data from')
parser.add_argument('-t', '--transactions', type=int, default=100, help='Maximum possible number of transactions to load per customer per time interval')
parser.add_argument('-i', '--increment', type=int, default=5, help='Time interval to increment from starting time')
args = parser.parse_args()

countries = ["UK", "US", "DE", "IE"]
currencies = ["EUR", "USD", "GBP"]
stp = [True, False]
methods = ["VISA", "AMEX", "CASH", "CHECK", "MC", "PAYPAL", "ACH"]
customers = []

count = 0

while (count < args.customers):
    customers.append(random_string())
    count = count + 1
    
processing_time = datetime.utcnow() - timedelta(minutes=args.minutes)

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

while processing_time < datetime.utcnow():
    processing_time = processing_time + timedelta(seconds=args.increment)
    print(processing_time)

    customer_cnt = random.randint(1,args.customers)

    cloop = 0
    while cloop < customer_cnt:
        customer = random.choice(customers)
        cloop = cloop + 1
        txn_cnt = random.randint(1, args.transactions)
        tloop = 0
        while tloop < txn_cnt:
            stpVal = random.choice(stp)
            jsonData = build_json(
                'payments',
                customer,
                random.choice(countries), 
                random.choice(methods),
                stpVal,
                random.choice(currencies),
                random.randint(100,5000000), 
                processing_time.isoformat())
            client.write_points(jsonData)
            
            if (stpVal):
                jsonData = build_json(
                    'stp_txns',
                    customer,
                    random.choice(countries),
                    random.choice(methods),
                    stpVal,
                    random.choice(currencies),
                    random.randint(100,5000000),
                    processing_time.isoformat())
                client.write_points(jsonData)

            
            tloop = tloop + 1

