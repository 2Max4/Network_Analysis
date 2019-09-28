import os
import signal
import speedtest
import time
import sys
import pandas as pd
from pythonping import ping

# User defines webpage and interval
url = input("Bitte geben Sie die URL für den Ping Test ein: ")
interval = int(input("Wie lange soll das Intervall der Abfragen sein (in Sekunden)? "))
ping_file_name = "ping_test.csv"
speed_test_file_name = "speed_test.csv"
direc = "Data"
ping_file_path = os.path.join(direc, ping_file_name)
speed_test_file_path = os.path.join(direc, speed_test_file_name)

# Take 5 threats as default value
threats = 5

# check if a ping_test file already exists
if "ping_test.csv" not in os.listdir("./" + direc):
    df_my_ping = pd.DataFrame(columns=["date", "min", "max", "avg", "url"])
else:
    df_my_ping = pd.read_csv(ping_file_path, index_col=0)

# Check if speed_test file already exists and create dataframe
if speed_test_file_name not in os.listdir("./" + direc):
    df_my_speed = pd.DataFrame(columns=["date", "ping", "downstream", "upstream", "serverState", "sponsor", "your_isp"])
else:
    df_my_speed = pd.read_csv(speed_test_file_path, index_col=0)


# Main-Part of speed check, take standard values, find best server (would be changeable to) and convert up/downstream
def get_speed_results_as_df(threads):
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    results_dict = s.results.dict()

    # Taking relevant values out results_dict{}
    speed_test_ping = int(results_dict["ping"])
    downstream = int(results_dict["download"]) / 1024
    upstream = int(results_dict["upload"]) / 1024
    server_state = results_dict["server"]["country"]
    sponsor = results_dict["server"]["sponsor"]
    your_isp = results_dict["client"]["isp"]

    # Return DataFrame filled by up/downstream, address and create timestamp
    return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S",
                                                time.localtime())],
                         "ping": [speed_test_ping],
                         "downstream": [downstream],
                         "upstream": [upstream],
                         "address": [server_state],
                         "sponsor": [sponsor],
                         "your_isp": [your_isp]})


# Function that performs ping test and returns Data Frame
def get_ping_as_df(ping_url):
    my_ping = ping(ping_url)
    return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())],
                         "min": [my_ping.rtt_min_ms],
                         "max": [my_ping.rtt_max_ms],
                         "avg": [my_ping.rtt_avg_ms],
                         "url": [ping_url]})


# Function gets executed when keyboard interrupt occures and makes sure that all reuslts are saved
def keyboard_interrupt_handler(signal, frame):
    print("\n**************************\n\n*** Keyboard interrupt *** \n \n**************************\n")
    print("Saving files to "+str(ping_file_path)+".")
    df_my_ping.to_csv(ping_file_path)
    print("Saving files to "+str(speed_test_file_path)+".")
    df_my_speed.to_csv(speed_test_file_path)
    sys.exit(0)


# Execution of infinit loop and catch if keyboard interrupts --> afterwarts persistent storage as csv
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

print("#### Currently analyzing the network ####")
while True:
    test_result = get_ping_as_df(url)
    if test_result["max"].max() > 10:
        df_my_speed = df_my_speed.append(get_speed_results_as_df(threats), ignore_index=True)
    df_my_ping = df_my_ping.append(test_result, ignore_index=True)
    if int(time.strftime("%M", time.localtime())) % 10 == 0:
        df_my_ping.to_csv(ping_file_path)
        df_my_speed.to_csv(speed_test_file_path)
    time.sleep(interval)
