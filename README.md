# Network_Analysis
This project is still under development and will be maintained mainly during the Hacktoberfest. The following guide helps you to begin with the current state of project and will be continually updated. If you are looking for a project to contribute to during the Hacktoberfest you are highly welcome to join our project. See "Dev Guide" for more information.


## Purpose of the Project
Collection of useful scripts to analyze the local network and evaluate network speed and velocity. The project helps you plot interactive graphs of network analysis. It is also capable to send you the same via email.

# Dev Guide
For everyone who is interested in being part of this project - feel free to grab an open issue. Generally, it is a good idea to first check whether someone else is already working on this issue and offer him help. If you've got any questions - always feel free to ask them.

Important: Please make sure to ALWAYS do your Pull Requests on Branch Testing - if everything runs smoothly, we will merge it to the master.



# User Guide
The Folder Data will contain all data that has been collected during the network tests (currently only ping test supported). All files that are stored in Data will not be deleted. Instead all new data will be appended to the existing existing file. Please make sure to not push your custom data collection to the GitRepo but include it in the .gitignore.


## Getting Started
1. Clone the git repository.
2. Make sure Python 3.7 is installed in the system.
3. Install the required Python packages. This can be done using `sudo pip3 install -r requirements.txt`.
4. Run the test. This can be done using `sudo python3 run_test.py` along with the arguments. The list of valid arguments can be found by running `sudo python3 run_test.py --help`.
5. After running the test for desired amount of time, send keyboard interrupt by pressing `Ctrl + C` twice. The data should get stored in the `Data` folder while  the graph should get stored in `webpage/figures` folder.
6. Open `webpage/index.html` in the browser to view the interactive graphs.

## Run Network Analysis
1. Make sure to complete all steps from the section Getting Started
2. Run network test with weekly email reporting by using a gmail account: `sudo python3 network_cli.py`
3. To get further information about possible options use  `sudo python3 network_cli.py --help`
