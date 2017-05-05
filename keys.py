# 1) Destination node generates public key and private key
# 2) Sends public key over to source node
# 3) Source node encrypts message using public key
# 4) Source node generates path to get to destination node
# 5) Message is sent along path until destination node receives encrypted message
# 6) Destination node using private key to decrypt message 

# Destination Node
from Crypto.PublicKey import RSA
from Crypto import Random
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
public_key = key.publickey().exportKey()
print(type(public_key))
#Send public key in string format to source node

# Source node
new_key = RSA.importKey(public_key)
encrypted = new_key.encrypt('NoSanaNoLife', 32)

# Send encrypted message back to destination node

#Destination Node
msg = key.decrypt(encrypted)
print msg