# Network_Analysis
Collection of useful scripts to analyse the local network and evaluate network speed and velocity

# Dev Guide
For everyone who is interested in beeing part of this project - feel free to grab an open issue. Generally it is a good idea to first check wheather someone else is already working on this issue and offer him help. If you've got any questions - always feel free to ask them.

Important: Please make sure to ALWAYS do your Pull Requests on Branch Testing - if everything runs smoothly we will merge it to the master.

# User Guide
The Folder Data will contain all data that has been collected during the network tests (currently only ping test supported). All files that are stored in Data will not be deleted. Instead all new data will be appended to the existing existing file. Please make sure to not push your custom data collection to the GitRepo but include it in the .gitignore.

# Starting Network Analysis
Currently there are different types of Network Analysis available. You can choose between a ping- and a speed test - both as .py files as well as .ipynb files. As a third option there is a small programm called network analysis which checks your ping at a custom intervall and depending on your ping time it then checks the actual speed of your internet connection. All results are again written in the Data folder from where they can be accessed and be used for further (statistical) tests. 
