# Dual-Eye-Tracking
This program shares real-time data among computers with TCP sockets

### Usage
* Set up one or more computers that share data with each other. One computer needs to be the server.
* Change `host` in `net_constants.py` to the ip address of the server.
* Change the `get_data()` and `display(data)` functions in `utilities.py` to reflect how the data are obtained and how they are displayed on the other clients' screen.
* If necessary, integrate the client as a part of the experiment program:
  * Delete the `main` part at the end of client.py
  * `import client` in the experiment file
  * Insert the following lines in the experiment file where the dual eye tracking should start  
    `client_thread = Client()`  
    `client_thread.start()`
* Run `server.py` on the server computer
* Run `client.py` (or the experiment file if integrated) on the client computers
