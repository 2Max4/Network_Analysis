#!/usr/bin/env python
# coding: utf-8

import os
import signal
import time
import pandas as pd
from pythonping import ping


# User defines webpage and interval
url = input("Bitte geben Sie die URL ein: ")
interval = int(input("Wie lange soll das Intervall der Abfragen sein (in Sekunden)? "))
file_name = "ping_test.csv"
direc = "Data"
file_path = direc+"/"+file_name

if "ping_test.csv" not in os.listdir("./"+direc):
    df_my_ping = pd.DataFrame(columns=["date", "min", "max", "avg", "url"])
else:
    df_my_ping = pd.read_csv(file_path, index_col=0)


def get_ping_as_df(url):
    my_ping = ping(url)
    return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())],
                         "min": [my_ping.rtt_min_ms],
                         "max": [my_ping.rtt_max_ms],
                         "avg": [my_ping.rtt_avg_ms],
                         "url": [url]})


# Function gets executed when keyboard interrupt occures
def keyboard_interrupt_handler(signal, frame):
    print("Keyboard interrupt - saving files to ping_test.csv.")
    df_my_ping.to_csv(file_path)
    exit(0)


# Execution of infinit loop and catch if keyboard interrupts --> afterwarts persistent storage as csv
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

print("#### Currently analyzing the network ####")
while True:
    df_my_ping = df_my_ping.append(get_ping_as_df(url), ignore_index=True)
    if int(time.strftime("%M", time.localtime()))%10 == 0:
        df_my_ping.to_csv(file_path)
    time.sleep(interval)


# Transform all dates to datetime format
df_my_ping["date"] = pd.to_datetime(df_my_ping["date"])
