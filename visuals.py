import pandas as pd
import sys
import os
import holoviews as hv
from holoviews import opts, dim, Palette
import configparser

# Define default layout of graphs
hv.extension('bokeh')

opts.defaults(
    opts.Bars(xrotation=45, tools=['hover']),
    opts.BoxWhisker(width=700, xrotation=30, box_fill_color=Palette('Category20')),
    opts.Curve(width=700, tools=['hover']),
    opts.GridSpace(shared_yaxis=True),
    opts.Scatter(width=700, height=500, color=Palette('Category20'), size=dim('growth')+5, tools=['hover'],alpha=0.5, cmap='Set1'),
    opts.NdOverlay(legend_position='left'))


# Initializes the figures path in webpage for the diagram output
if os.path.isdir(os.path.join("webpage","figures")) is False:
    os.mkdir(os.path.join("webpage","figures"))
    print("Path 'figures' created successfully")
else:
    print("Path 'figures' initialized")


class InteractivePlots:

    def __init__(self):

        # Load basic configurations
        config = configparser.ConfigParser()

        try:
            config.read('config_a.ini')
            # Get values from configuration file
            self.upper_acceptable_ping_bound = float(config['DEFAULT']['upper_acceptable_ping_bound'])
            self.upper_ping_issue_bound = float(config['DEFAULT']['upper_ping_issue_bound'])
            self.acceptable_network_speed = float(config['DEFAULT']['acceptable_network_speed'])
        except:
            # In case no config-file is found or another reading error occured
            print("Configuration file not found/readable.")
            print("Creating a new configuration file.")
            # Creating new file with standard values
            config['DEFAULT'] = {'upper_acceptable_ping_bound': '10',
                                 'upper_ping_issue_bound': '99999',
                                 'acceptable_network_speed': '16'}
            with open('config_a.ini', 'w') as configfile:
                config.write(configfile)
            print("New configuration file was created. Running on default parameters, please restart for changes.")

            #set default values to continue with program
            self.upper_acceptable_ping_bound = float(config['DEFAULT']['upper_acceptable_ping_bound'])
            self.upper_ping_issue_bound = float(config['DEFAULT']['upper_ping_issue_bound'])
            self.acceptable_network_speed = float(config['DEFAULT']['acceptable_network_speed'])

        try:
            self.df_ping = pd.read_csv("Data/ping_test.csv", index_col=0)
            self.df_speed_test = pd.read_csv("Data/speed_test.csv", index_col=0)

            self.df_ping["date"] = pd.to_datetime(self.df_ping["date"], format="%d.%m.%Y %H:%M:%S")
            self.df_speed_test["date"] = pd.to_datetime(self.df_speed_test["date"], format="%d.%m.%Y %H:%M:%S")

        except:
            print("Error while searching for files. Please perform network-test first.")
            sys.exit(0)

        # Clear data from issues
        self.df_ping = self.df_ping[self.df_ping["max"] != self.upper_ping_issue_bound]
        self.df_speed_test = self.df_speed_test[self.df_speed_test["ping"] != self.upper_ping_issue_bound]

    def generate_graph_ping_times_with_extreme_outliers(self):
        fig_all_max_ping = hv.Curve((self.df_ping["date"], self.df_ping["max"]),
                                    "Date",
                                    "Ping in ms",
                                    label="All messured pings")
        fig_dot_over_upper_bound = hv.Scatter(
            (self.df_ping["date"][self.df_ping["max"] > self.upper_acceptable_ping_bound],
             self.df_ping["max"][self.df_ping["max"] > self.upper_acceptable_ping_bound]),
            "Date",
            "Max_Ping_Time",
            label="Highlight pings over {} ms".format(
                str(self.upper_acceptable_ping_bound))).opts(opts.Scatter(color="red", size=10))

        fig_ping_times_with_extreme_outliers = (fig_all_max_ping *
                                                fig_dot_over_upper_bound).opts(
            legend_position="top_left",
            title="All Max. Ping Times in ms", padding=0.05)
        # Safe newly generated plot
        hv.save(fig_ping_times_with_extreme_outliers,
                os.path.join("webpage", "figures",
                             "fig_ping_times_with_extreme_outliers.html"),
                backend='bokeh')

    def generate_graph_ping_times_without_extreme_outliers(self):
        fig_ping_without_extreme_outliers = hv.Curve(
            (self.df_ping["date"][self.df_ping["max"] < 1000],
             self.df_ping["max"][self.df_ping["max"] < 1000]), "Date", "Ping in ms", label="All ping times less then 1000 ms")

        fig_ping_highlight_max = hv.Scatter(
            (self.df_ping["date"][self.df_ping["max"] > self.upper_acceptable_ping_bound][self.df_ping["max"] < 1000],
             self.df_ping["max"][self.df_ping["max"] > self.upper_acceptable_ping_bound][self.df_ping["max"] < 1000]),
            "Date",
            "Max_Ping_Time",
            label="Highlight pings over {} ms".format(str(self.upper_acceptable_ping_bound))
        ).opts(color="red", size=10)

        fig_ping_times_without_extreme_outliers = (fig_ping_without_extreme_outliers * fig_ping_highlight_max).opts(
            title="All Max. Ping Times in ms without extreme outlieres",
            legend_position="top_left",
            padding=0.05)

        # Safe newly generated plot
        hv.save(fig_ping_times_without_extreme_outliers,
                os.path.join("webpage", "figures", "fig_ping_times_without_extreme_outliers.html"), backend='bokeh')

    def generate_graph_network_speed(self):
        pingbound_network_test = self.df_speed_test["ping"].min()

        fig_network_speed_below_pingbound = hv.Curve(
            (self.df_speed_test["date"], self.df_speed_test["downstream"] / 1000),
            "Date",
            "Network Speed",
            label="Messured downlink speed when ping below {} ms".format(
                str(pingbound_network_test)))

        fig_highlight_below_acceptable_network_speed = hv.Scatter(
            (self.df_speed_test["date"][
                 self.df_speed_test["downstream"] / 1000 < self.acceptable_network_speed],
             self.df_speed_test["downstream"][
                 self.df_speed_test["downstream"] / 1000 < self.acceptable_network_speed] / 1000),
            "Date",
            "Network Speed",
            label="Highlight downstream speed below {} mbit/s".format(
                str(self.acceptable_network_speed))).opts(color="red", size=10)

        fig_horizontal_marker = hv.HLine(
            self.acceptable_network_speed,
            label="Acceptable network speed at {} mbit/s".format(
                str(self.acceptable_network_speed))).opts(color="black")

        fig_upstream_below_ping_bound = hv.Curve(
            (self.df_speed_test["date"], self.df_speed_test["upstream"] / 1000),
            "Date",
            "Network Speed",
            label="Messured uplink when ping below {} ms".format(
                str(pingbound_network_test))).opts(color="purple")

        fig_network_speeds_under_upper_bound = (
                fig_network_speed_below_pingbound *
                fig_highlight_below_acceptable_network_speed * fig_upstream_below_ping_bound * fig_horizontal_marker
        ).opts(
            title="Network Speed when Ping below {} ms".format(pingbound_network_test),
            legend_position="top_left",
            padding=0.05)

        # Safe newly generated plot
        hv.save(fig_network_speeds_under_upper_bound,
                os.path.join("webpage", "figures",
                             "fig_network_speeds_under_upper_bound.html"),
                backend='bokeh')

    # generates all plots and saves them
    def generate_and_save_all_plots(self):
        self.generate_graph_network_speed()
        self.generate_graph_ping_times_with_extreme_outliers()
        self.generate_graph_ping_times_without_extreme_outliers()