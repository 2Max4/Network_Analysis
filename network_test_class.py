import os
import speedtest
import time
import sys
import shutil
import pandas as pd
from pythonping import ping
import argparse
import logging
import traceback
from visuals import InteractivePlots

# define logger
main_logger = logging.getLogger("main_logger")
main_logger.setLevel("WARNING")


# Create PingTest class
class NetworkTest:

    def __init__(self):

        parser = argparse.ArgumentParser()
        parser.add_argument("--interval", type=int, default=5, help="Interval in which ping test should be performed")
        parser.add_argument("--ping_target", type=str, default="www.google.de", help="Server that should be pinged")
        parser.add_argument("--threads", type=int, default=1,
                            help="Amount of threads to be used while performing speed test")
        parser.add_argument("--path", type=str, default="Data",
                            help="Folder name in which the results should be stored")
        parser.add_argument("--ping_file_name", type=str, default="ping_test.csv",
                            help="Name of csv file for ping results")
        parser.add_argument("--speed_test_file_name", type=str, default="speed_test.csv",
                            help="Name of csv file for speed test results")
        parser.add_argument("--clear", type=bool, default=False,
                            help="If set to true all old results will be moved to archive. - Default = False")

        args = parser.parse_args()

        self.interval = args.interval
        self.ping_target = args.ping_target
        self.threads = args.threads
        self.path = args.path
        self.ping_file_name = args.ping_file_name
        self.speed_test_file_name = args.speed_test_file_name
        self.clear = args.clear
        self.ping_file_path = os.path.join(self.path, self.ping_file_name)
        self.speed_test_file_path = os.path.join(self.path, self.speed_test_file_name)

        # check if old files need to be moved in new dir.
        # If dir archive dosen't exist - create new one
        if args.clear is True:

            if os.path.isdir(os.path.join(args.path, "archive")) is False:

                # create archive folder
                os.mkdir(os.path.join(args.path, "archive"))
                date = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())

                new_ping_name = "".join(
                    (args.ping_file_name.split(".")[0], date, ".", args.ping_file_name.split(".")[1]))
                new_speed_test_name = "".join(
                    (args.speed_test_file_name.split(".")[0], date, ".", args.speed_test_file_name.split(".")[1]))

                shutil.copyfile(os.path.join(args.path, args.ping_file_name),
                                os.path.join(args.path, "archive", new_ping_name))
                shutil.copyfile(os.path.join(args.path, args.speed_test_file_name),
                                os.path.join(args.path, "archive", new_speed_test_name))

            else:
                # Error da nicht erkannt wird ob ping_file_name in i!

                date = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())

                new_ping_name = "".join(
                    (args.ping_file_name.split(".")[0], date, ".", args.ping_file_name.split(".")[1]))
                new_speed_test_name = "".join(
                    (args.speed_test_file_name.split(".")[0], date, ".", args.speed_test_file_name.split(".")[1]))

                shutil.copyfile(os.path.join(args.path, args.ping_file_name),
                                os.path.join(args.path, "archive", new_ping_name))
                shutil.copyfile(os.path.join(args.path, args.speed_test_file_name),
                                os.path.join(args.path, "archive", new_speed_test_name))

        # check if a ping_test file already exists
        if "ping_test.csv" not in os.listdir("./" + self.path):
            self.df_my_ping = pd.DataFrame(columns=["date", "min", "max", "avg", "url"])
        else:
            self.df_my_ping = pd.read_csv(self.ping_file_path, index_col=0)

        # Check if speed_test file already exists and create dataframe
        if self.speed_test_file_name not in os.listdir("./" + self.path):
            self.df_my_speed = pd.DataFrame(
                columns=["date", "ping", "downstream", "upstream", "serverState", "sponsor", "your_isp"])
        else:
            self.df_my_speed = pd.read_csv(self.speed_test_file_path, index_col=0)

    # Main-Part of speed check, take standard values, find best server (would be changeable to) and convert up/downstream
    def get_speed_results_as_df(self):

        try:
            s = speedtest.Speedtest()
            s.get_servers()
            s.get_best_server()
            s.download(threads=self.threads)
            s.upload(threads=self.threads)
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
    def get_ping_as_df(self):
        try:
            my_ping = ping(self.ping_target)

            return pd.DataFrame({"date": [time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())],
                                 "min": [my_ping.rtt_min_ms],
                                 "max": [my_ping.rtt_max_ms],
                                 "avg": [my_ping.rtt_avg_ms],
                                 "url": [self.ping_target]})
        except Exception as e:
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
    def keyboard_interrupt_handler(self, signal):
        print("\n**************************\n\n"
              "*** Keyboard interrupt *** \n \n**************************\n")
        print("Saving files to " + str(self.ping_file_path) + ".")
        self.df_my_ping.to_csv(self.ping_file_path)
        print("Saving files to " + str(self.speed_test_file_path) + ".")
        self.df_my_speed.to_csv(self.speed_test_file_path)
        sys.exit(0)

    '''Function starts networktest in endless loop. To exit the loop and safe results Ctrl + C must be pressed 
            twice '''

    def run_network_test(self):
        print("#### Currently analyzing the network ####")
        try:
            while True:
                test_result = self.get_ping_as_df()
                if test_result["max"].max() > 10:
                    self.df_my_speed = self.df_my_speed.append(self.get_speed_results_as_df(),
                                                               ignore_index=True, sort=False)
                self.df_my_ping = self.df_my_ping.append(test_result, ignore_index=True, sort=False)
                if int(time.strftime("%M", time.localtime())) % 10 == 0:
                    self.to_csv(self.ping_file_path)
                    self.df_my_speed.to_csv(self.speed_test_file_path)
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n**************************\n\n"
                  "*** Keyboard interrupt *** \n \n**************************\n")
            print("Saving files to " + str(self.ping_file_path) + ".")
            self.df_my_ping.to_csv(self.ping_file_path)
            print("Saving files to " + str(self.speed_test_file_path) + ".")
            self.df_my_speed.to_csv(self.speed_test_file_path)
            print("\n**************************\n\n"
                  "*** Press Controle -C to finally exit ***"
                  "\n**************************\n")

    def run_network_test_and_generate_graphs(self):
        visuals = InteractivePlots()
        print("#### Currently analyzing the network ####")
        try:
            while True:
                test_result = self.get_ping_as_df()
                if test_result["max"].max() > 10:
                    self.df_my_speed = self.df_my_speed.append(self.get_speed_results_as_df(),
                                                               ignore_index=True, sort=False)
                self.df_my_ping = self.df_my_ping.append(test_result, ignore_index=True, sort=False)
                if int(time.strftime("%M", time.localtime())) % 10 == 0:
                    self.to_csv(self.ping_file_path)
                    self.df_my_speed.to_csv(self.speed_test_file_path)
                    visuals.generate_and_save_all_plots()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n**************************\n\n"
                  "*** Keyboard interrupt *** \n \n**************************\n")
            print("Saving files to " + str(self.ping_file_path) + ".")
            self.df_my_ping.to_csv(self.ping_file_path)
            print("Saving files to " + str(self.speed_test_file_path) + ".")
            self.df_my_speed.to_csv(self.speed_test_file_path)
            visuals.generate_and_save_all_plots()
            print("\n**************************\n\n"
                  "*** Press Controle -C to finally exit ***"
                  "\n**************************\n")


# Example Usage

# my_ping_test = NetworkTest()
# run network test in infinite loop
# my_ping_test.run_network_test_and_generate_graphs()

