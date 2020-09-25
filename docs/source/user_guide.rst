User Guide
^^^^^^^^^^

The Folder Data will contain all data that has been collected during the network tests (currently only ping test supported). All files that are stored in Data will not be deleted. Instead all new data will be appended to the existing existing file. Please make sure to not push your custom data collection to the GitRepo but include it in the .gitignore.


Getting Started
---------------

1. Clone the git repository.
2. Make sure Python 3.7 is installed in the system.
3. Install the required Python packages. This can be done using `sudo pip3 install -r requirements.txt`.
4. Run the test. This can be done using `sudo python3 run_test.py` along with the arguments. The list of valid arguments can be found by running `sudo python3 run_test.py --help`.
5. After running the test for desired amount of time, send keyboard interrupt by pressing `Ctrl + C` twice. The data should get stored in the `Data` folder while  the graph should get stored in `webpage/figures` folder.
6. Open `webpage/index.html` in the browser to view the interactive graphs.

Run Network Analysis
--------------------

1. Make sure to complete all steps from the section Getting Started
2. Run network test with weekly email reporting by using a gmail account: `sudo python3 network_cli.py`
3. To get further information about possible options use  `sudo python3 network_cli.py --help`

Getting started with the GUI
----------------------------

Prerequisites
+++++++++++++

You'll need PyQt5 and other libraries from requirements.txt

Running
+++++++

Navigate to the project's root folder, and run `python3 network_qt5.py` with root priviledges.

