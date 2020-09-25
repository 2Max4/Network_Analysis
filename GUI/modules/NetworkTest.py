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
import configparser

from PyQt5.QtCore import pyqtSignal, QObject

from modules.visuals import InteractivePlots

class Communicate(QObject):
    GUI_signal = pyqtSignal(str)

# define logger
main_logger = logging.getLogger("main_logger")
main_logger.setLevel("WARNING")

class NetworkTest:

    def __init__(self, defaults, callbackFunc):
        self.interval = defaults["interval"]
        self.ping_target = defaults["ping_target"]
        self.threads = defaults["threads"]
        self.path = defaults["path"]
        self.config_path = os.path.join(self.path, "modules", "config_a.ini")
        self.ping_file_name = defaults["ping_file_name"]
        self.speed_test_file_name = defaults["speed_test_file_name"]
        self.clear = defaults["clear"]
        self.ping_file_path = os.path.join(self.path, "Data", self.ping_file_name)
        self.speed_test_file_path = os.path.join(self.path, "Data", self.speed_test_file_name)

        self.doPingTest = True
        self.doSpeedTest = True

        self.runningTest = False

        self.readConfig()
        self.visuals = InteractivePlots(self.path, self.ping_file_path, self.speed_test_file_path)

        self.src = Communicate()
        self.src.GUI_signal.connect(callbackFunc)

    def readConfig(self):
        config = configparser.ConfigParser()

        try:
            config.read(self.config_path)
            # Get values from configuration file
            self.save_every = float(config['DEFAULT']['save_every'])
            self.ping_max_threshold = float(config['DEFAULT']['ping_max_threshold'])
        except:
            # In case no config-file is found or another reading error occured
            print("Configuration file not found/readable.")
            sys.exit(0)


    def updateTestVariables(self, updatedVariables):
        print(updatedVariables)
        self.doPingTest = updatedVariables["doPingTest"]
        self.doSpeedTest = updatedVariables["doSpeedTest"]
        self.interval = updatedVariables["interval"]
        self.ping_target = updatedVariables["ping_target"]
        self.threads = updatedVariables["threads"]
        self.path = updatedVariables["path"]
        self.ping_file_name = updatedVariables["ping_file_name"]
        self.speed_test_file_name = updatedVariables["speed_test_file_name"]
        self.clear = updatedVariables["clear"]
        self.ping_file_path = os.path.join(self.path, "Data", self.ping_file_name)
        self.speed_test_file_path = os.path.join(self.path, "Data", self.speed_test_file_name)

    # check if old files need to be moved in new dir.
    # If dir archive dosen't exist - create new one
    def archiveFiles(self):
        if os.path.isdir(os.path.join(self.path, "Data", "archive")) is False:
            # create archive folder
            os.mkdir(os.path.join(self.path, "Data", "archive"))

        date = time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())
        new_ping_name = "".join(
            (self.ping_file_name.split(".")[0], date, ".", self.ping_file_name.split(".")[1]))
        new_speed_test_name = "".join(
            (self.speed_test_file_name.split(".")[0], date, ".", self.speed_test_file_name.split(".")[1]))

        shutil.move(os.path.join(self.path, "Data", self.ping_file_name),
                        os.path.join(self.path, "Data", "archive", new_ping_name))
        shutil.move(os.path.join(self.path, "Data", self.speed_test_file_name),
                        os.path.join(self.path, "Data", "archive", new_speed_test_name))

    # check if old dataframe exists else create new one
    def createDataFrames(self):
        # check if a ping_test file already exists
        if(self.doPingTest):
            if self.ping_file_name not in os.listdir(os.path.join(self.path, "Data")):
                self.df_my_ping = pd.DataFrame(columns=["date", "min", "max", "avg", "url"])
            else:
                self.df_my_ping = pd.read_csv(self.ping_file_path, index_col=0)

        # Check if speed_test file already exists and create dataframe
        if(self.doSpeedTest):
            if self.speed_test_file_name not in os.listdir(os.path.join(self.path, "Data")):
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

    def startTest(self):
        self.runningTest = True

    def endTest(self):
        self.runningTest = False


    '''Function starts networktest in endless loop. To exit the loop and safe results Ctrl + C must be pressed twice '''
    def run_network_test(self):
        print("#### Currently analyzing the network ####")
        newTest = True
        lastSaved = time.time()
        try:
            while True:
                # print("Thread Running " + str(time.time()))
                msgForGui = 'Message from NetworkTest'
                self.src.GUI_signal.emit(msgForGui)
                if(self.runningTest):
                    print("Test is running")
                    if(newTest):
                        if self.clear is True:
                            self.archiveFiles()
                        self.createDataFrames()
                        newTest = False
                    test_result = self.get_ping_as_df()
                    if(self.doPingTest):
                        self.df_my_ping = self.df_my_ping.append(test_result, ignore_index=True, sort=False)
                    if(self.doSpeedTest):
                        # only perform speed test if ping max rtt greater than threshold so as not to consume excessive bandwidth
                        if test_result["max"].max() > self.ping_max_threshold:
                            self.df_my_speed = self.df_my_speed.append(self.get_speed_results_as_df(), ignore_index=True, sort=False)

                    # save files every n seconds (defined in congif)
                    if int(time.time() - lastSaved) > self.save_every:
                        self.df_my_ping.to_csv(self.ping_file_path)
                        self.df_my_speed.to_csv(self.speed_test_file_path)
                        lastSaved = time.time()
                else:
                    if(newTest is False):
                        if(self.doPingTest):
                            print("Saving files to " + str(self.ping_file_path) + ".")
                            self.df_my_ping.to_csv(self.ping_file_path)
                        if(self.doSpeedTest):
                            print("Saving files to " + str(self.speed_test_file_path) + ".")
                            self.df_my_speed.to_csv(self.speed_test_file_path)
                        newTest = True
                time.sleep(self.interval)

        except Exception as e:
            print("************************************")

            main_logger.warning(e)
            traceback.print_exc()
            print("************************************\n\n")

    def generate_and_save_all_plots(self):
        self.visuals.updateTestVariables(self.path, self.ping_file_path, self.speed_test_file_path)
        self.visuals.generate_and_save_all_plots()
