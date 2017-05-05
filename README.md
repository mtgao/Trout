# Trout

Trout is a TOR routing POC project that aims to do the following:

  - Allow clients (nodes) to join or leave our service cluster
  - Send messages between clients using onion-esque routing with intermediary nodes
  - Ecnrypt messages with RSA public/private key encryption

# Node Architecture

For our cluster, we decided on a leaderless system. Each node owns their own membership list that contains the currently active nodes in our service cluster. To handle joins and leaves, we use an introducer node on a fixed IP address. We will assume for the scope of our project that the introducer node will never fail.

Membership list contain a timestamp of when the list was last updated and a dictionary of members where the key is username and the value is respective IP. 

When a new client node first starts, it attempts to join our cluster by contacting the introducer node. The following occurs: