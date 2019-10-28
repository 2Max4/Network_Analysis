# Network_Analysis
Collection of useful scripts to analyze the local network and evaluate network speed and velocity

# User Guide
The Folder Data will contain all data that has been collected during the network tests (currently only ping test supported). All files that are stored in Data will not be deleted. Instead all new data will be appended to the existing existing file. Please make sure to not push your custom data collection to the GitRepo but include it in the .gitignore.

# Starting Network Analysis
Currently there are different types of Network Analysis available. You can choose between a ping- and a speed test - both as .py files as well as .ipynb files. As a third option there is a small program called network analysis which checks your ping at a custom interval and depending on your ping time it then checks the actual speed of your internet connection. All results are again written in the Data folder from where they can be accessed and be used for further (statistical) tests. 
