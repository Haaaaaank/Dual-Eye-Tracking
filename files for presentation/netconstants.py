BUFFER_SIZE = 128    # TODO should be multiply of the size of eye position; use previous send_all()?

DEFAULT_HOST = 'localhost'
host = DEFAULT_HOST
PORT = 50000
SOCKET_BACKLOG = 5
CLIENT_SOCKET_TIMEOUT = 0.05  # TODO probably should be higher if the internet connection is slow?
SERVER_SOCKET_TIMEOUT = 1  #

# command strings
CMD_RENAME = "/name"
CMD_QUIT = "/quit"
CMD_START = "/start"