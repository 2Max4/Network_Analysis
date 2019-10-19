import os
import signal
import speedtest
import time
import sys
import shutil
import pandas as pd
from pythonping import ping
import argparse
import logging
import traceback

main_logger = logging.getLogger("main_logger")
main_logger.setLevel("WARNING")


#User defines webpage and intervall
parser = argparse.ArgumentParser()
parser.add_argument("--intervall", type=int, default=5, help="Intervall in which ping test should be performed")
parser.add_argument("--ping_target", type=str, default="www.google.de", help="Server that should be pinged")
parser.add_argument("--threads", type=int, default=1, help="Amount of threads to be used while performing speed test")
parser.add_argument("--path", type=str, default="Data", help="Folder name in which the results should be stored")
parser.add_argument("--ping_file_name", type=str, default="ping_test.csv", help="Name of csv file for ping results")
parser.add_argument("--speed_test_file_name", type=str, default="speed_test.csv", help="Name of csv file for speed test results")
parser.add_argument("--clear", type=bool, default=False, help="If set to true all old results will be moved to archive. - Default = False")

args = parser.parse_args()


# User defines webpage and intervall
url = args.ping_target
intervall = args.intervall
ping_file_name = args.ping_file_name
speed_test_file_name = args.speed_test_file_name
direc = args.path
ping_file_path = os.path.join(direc, ping_file_name)
speed_test_file_path = os.path.join(direc, speed_test_file_name)

# check if old files need to be moved in new dir.
# If dir archive dosen't exist - create new one

if args.clear is True:

    if os.path.isdir(os.path.join(args.path, "archive")) is False:

        # create archive folder
        os.mkdir(os.path.join(args.path, "archive"))
        date = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())

        new_ping_name = "".join((args.ping_file_name.split(".")[0], date, ".", args.ping_file_name.split(".")[1]))
        new_speed_test_name = "".join((args.speed_test_file_name.split(".")[0], date,".", args.speed_test_file_name.split(".")[1]))

        shutil.copyfile(os.path.join(args.path, args.ping_file_name), os.path.join(args.path, "archive", new_ping_name))
        shutil.copyfile(os.path.join(args.path, args.speed_test_file_name), os.path.join(args.path, "archive", new_speed_test_name))

    else:
        #Error da nicht erkannt wird ob ping_file_name in i!

        date = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())

        new_ping_name = "".join((args.ping_file_name.split(".")[0], date, ".", args.ping_file_name.split(".")[1]))
        new_speed_test_name = "".join(
            (args.speed_test_file_name.split(".")[0], date, ".", args.speed_test_file_name.split(".")[1]))

        shutil.copyfile(os.path.join(args.path, args.ping_file_name), os.path.join(args.path, "archive", new_ping_name))
        shutil.copyfile(os.path.join(args.path, args.speed_test_file_name),
                        os.path.join(args.path, "archive", new_speed_test_name))










# Take 5 threats as default value
threats = args.threads

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
def get_speed_results_as_df(speed_threads):

    try:
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download(threads=speed_threads)
        s.upload(threads=speed_threads)
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
    except Exception as e:
        print("************************************")
        main_logger.warning(e)
        traceback.print_exc()
        print("************************************\n\n")

        return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S",
                                                    time.localtime())],
                             "ping": [99999],
                             "downstream": [99999],
                             "upstream": [99999],
                             "address": [e],
                             "sponsor": [e],
                             "your_isp": [e]})


# Function that performs ping test and returns Data Frame
def get_ping_as_df(ping_url):
    try:
        my_ping = ping(ping_url)

        return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())],
                             "min": [my_ping.rtt_min_ms],
                             "max": [my_ping.rtt_max_ms],
                             "avg": [my_ping.rtt_avg_ms],
                             "url": [ping_url]})
    except PermissionError as e:
        print("************************************")

        main_logger.warning(e)
        traceback.print_exc()
        print("************************************\n\n")

        # Returns Data Frame with 99999 to show, that there is an error - exception gets pasted into URL
        return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())],
                             "min": [99999],
                             "max": [99999],
                             "avg": [99999],
                             "url": [e]})

    except AttributeError as e:
        print("************************************")

        main_logger.warning(e)
        traceback.print_exc()
        print("************************************\n\n")

        # Returns Data Frame with 99999 to show, that there is an error - exception gets pasted into URL
        return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())],
                             "min": [99999],
                             "max": [99999],
                             "avg": [99999],
                             "url": [e]})


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
        df_my_speed = df_my_speed.append(get_speed_results_as_df(threats), ignore_index=True, sort=False)
    df_my_ping = df_my_ping.append(test_result, ignore_index=True, sort=False)
    if int(time.strftime("%M", time.localtime())) % 10 == 0:
        df_my_ping.to_csv(ping_file_path)
        df_my_speed.to_csv(speed_test_file_path)
    time.sleep(intervall)
