# run server: server [port]
# run client: client [ip]:[port]

from snippets.lab3 import *
import sys

mode = sys.argv[1].lower().strip()
peers = [] #client has only 1 peer connected (server peer), server has more peer connected(client peer)

def send_message(msg, sender):
    if peers == []:
        print("No peer connected, message is lost")
    elif msg:
        for peer in peers:
            peer.send(message(msg.strip(), sender))
    else:
        print("Empty message, not sent")

def on_message_received(event, payload, connection, error):
    match event:
        case 'message':
            print(payload)
            if mode == 'server':
                for peer in peers:
                    if peer != connection:
                        peer.send(payload)

        case 'close':
            print(f"Connection with peer {connection.remote_address} closed")
            peers.remove(connection)
        case 'error':
            print(error)

if mode == 'server':
    port = int(sys.argv[2])

    def on_new_connection(event, connection, address, error):
        match event:
            case 'listen':
                print(f"Server listening on port {address[0]} at {', '.join(local_ips())}")
            case 'connect':
                print(f"Open ingoing connection from: {address}")
                connection.callback = on_message_received
                peers.append(connection)
            case 'stop':
                print(f"Stop listening for new connections")
            case 'error':
                print(error)

    server = Server(port, on_new_connection)
elif mode == 'client':
    remote_endpoint = sys.argv[2]
    try:
        peer = Client(address(remote_endpoint), on_message_received)
    except(Exception):
        print("Error in connection with server. Try again or try with another ip address.")
        exit(1)
    peers.append(peer)
    print(f"Connected to {peer.remote_address}")

username = input('Enter your username to start the chat:\n')
print('Type your message and press Enter to send it. Messages from other peers will be displayed below.')
while True:
    try:
        content = input()
        send_message(content, username)
    except (EOFError, KeyboardInterrupt):
        break
if mode == 'server':
    server.close()