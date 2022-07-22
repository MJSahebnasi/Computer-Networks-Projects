# Computer-Networks-Projects
two projects done in the Computer Networks course:

## simple-CS-P2P
receiving a file (.jpg) using both Client-Server and P2P methods:

Just run main.py .

### Client-Server:
The whole file is received through a TCP connection.

### P2P:
First, file metadata and peers addresses is retreived through a TCP connection (in order to get more peer addresses, several parallel requests will be sent).
Then a seperate parallel request (UDP) will be sent to each peer to get a part (block) of data.
Finally, all blocks will be agregated into one file.

## AutonomousSys-DistanceVector
In this project, our goal is to simulate a network of routers, running a routing algorithm (Distance Vector) on it, and trying to make the network dynamic. 
- Connected nodes (routers) can interact with each other: each node is both an always-listening server (waiting for other nodes to send messages) and a client (which sends messages to others). 
- The message each node sends to it's neighbors is either it's routing table or message announcing a change in the edges connected to the node.

After running main.py , you will see something like this:

[img]()

As you can see, there are several commands that you enter.
