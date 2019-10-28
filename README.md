# Network_Analysis
This project is still under development. The following guide helps to begin with the current state of project and will be updated soon.

## Purpose of the Project
Collection of useful scripts to analyze the local network and evaluate network speed and velocity. The project helps you plot interactive graphs of network analysis. It is also capable to send you the same via email.

## Getting Started
1. Clone the git repository.
2. Make sure Python3.7 is installed in the system.
3. Install the required Python packages. This can be done using `sudo pip3 install -r requirements.txt`.
4. Run the test. This can be done using `sudo python3 run_test.py` along with the arguments. The list of valid arguments can be found by running `sudo python3 run_test.py --help`.
5. After running the test for desired amount of time, send keyboard interrupt by pressing `Ctrl + C` twice. The data should get stored in the `Data` folder while  the graph should get stored in `webpage/figures` folder.
6. Open `webpage/index.html` in the browser to view the interactive graphs.
