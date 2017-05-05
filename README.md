# Trout

Trout is a TOR routing POC project that aims to do the following:

  - Allow clients (nodes) to join or leave our service cluster
  - Send messages between clients using onion-esque routing with intermediary nodes
  - Encrypt messages with RSA public/private key encryption

# Node Architecture

For our cluster, we decided on a leaderless system. Each node owns their own membership list that contains the currently active nodes in our service cluster. To handle joins and leaves, we use an introducer node on a fixed IP address. We will assume for the scope of our project that the introducer node will never fail.

Membership list contain a timestamp of when the list was last updated and a dictionary of members where the key is username and the value is respective IP. 

When a new client node first starts, it attempts to join our cluster by contacting the introducer node. The following occurs:

  - Send introducer node a join message with our own username and IP
  - Introducer node receives join message and sends back membership list in join-ack message
  - Client receives join ack and updates their membershiplist to reflect current cluster state

When a client wants to leave the cluster, they simply send a leave message to the introducer.

## Membership Consistency 

To maintain consistent membership list across all nodes, we use round-robin style pinging. In our ping function, we iterate through members of our membership list and send them a ping type message. When a node receives a ping message, it responds with a ping-ack. The sender of the original ping message waits for the ping-ack to confirm that the member is still alive. However, if a 3 second timeout period passes, we mark that member as failed and remove them from our membership list. For every ping message sent, we have our membership list attached with a timestamp of when it was last updated and on receipt of these messages, we make a comparison on our membership list with the one sent through the message. If the message list is more recently updated than our own, we replace our membership list with it. This ensures that changes to our membership list propogate through our cluster so that every node has a consistant view of cluster status.

## Listen and Ping Thread

Each node runs two threads for our described architecture to function correctly. The ping thread maintains our membership consistency as described above. The listen thread listens for connections and handles the different message types.

## Messages and Data Serialization

Our messages are standardized and defined in message.py. Each message contains 5 parts:

  - Header: message type
  - Timestamp: time of message creation
  - Memberlist: current membership list
  - Content: message content
  - Directions: route determined by our routing algorithm
   
To send message objects to our nodes, we have to serialize our data. To do so, we use the python pickle module to serialize the data before transmission and deserialize data upon receipt. 

## Routing Algorithm

One of the main purposes of our project was to create our own algorithm to send a message from a source node to a destination node using a minimum number of intermediary nodes. Creation of this route is split into the following steps:

  - Create a graph with vertexes as the members in the cluster
  - Create edges between every pair of vertices
  - Add random edge weight (1-50) for each edge to simulate hypothetical distances between nodes
  - Perform a shortest path search from our source to destination vertex witth a minimum number of intermediary node visits (min number of intermediary currently hard coded to 1 since we only had 3 linux machines to use) 

## Messaging Between Users

Using this routing algorithm, we have a path to send a message from user A to user B using intermediary nodes. For enhancing security, we use RSA encryption between the source and destination node. This is done through the following steps:

  - Destination node generates public key and private key
  - Sends public key over to source node
  - Source node encrypts message using public key
  - Source node generates path to get to destination
  - Message is sent along path until destination node receives encrypted message
  - Destination node using private key to decrypt message 

# Using Trout

Trout requires Pycrypto to run. 
```sh
$ sudo pip install pycrypto
```

To start a client node run:

```sh
$ cd Trout
$ python2 node.py username
```

where username can be replaced by your own username.

To start an introducer node simply include the -i flag prior to username (the introducer IP will have to be manually changed in node.py to reflect the ip of the machine running the introducer):

```sh
$ python2 node.py -i username
```

We support the use of the basic commands from the terminal once the client node is running.

Show current membership list:

```sh
$ show
```

Leave Cluster:

```sh
$ leave
```

Send message to another user:

```sh
$ send destination_user message
```

## Furtherwork 
  - Sometimes the ping ack messages aren't received due to the nature of UDP packets. We can improve this by attempting to ping a node more than once instead of a single attempt. 
  - Sometimes join messages aren't correctly recognized by the introducer node in which case the client has to restart to join properly. For this, we can improve our join routine to more reliably handle this type of situation.
  - Our routing algorithm can be improved by using actual network distances as the edge weights between nodes
  - We can improve the security of our sent messages by encrypting the message in layers by using all the public keys from every node in the message route. 
