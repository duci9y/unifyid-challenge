import requests
from Crypto.PublicKey import RSA

class RandomOrg(object):
    """A wrapper for requesting sequences of random bytes of arbitrary lengths
       from random.org."""
    def __init__(self, default_length=4000):
        self.cache = b''
        self.cache_index = 0
        self.default_length = default_length
    
    def generate(self, length):
        index = self.cache_index
        if self.cache and index < len(self.cache) + length:
            # there's unused bytes in the cache, return them
            result = self.cache[index:index + length]
            self.cache_index += length
            return result

        # new bytes needed
        print('Requesting bytes from random.org...')
        # format=f makes sure data downloaded is binary and not text
        response = requests.get('https://www.random.org/cgi-bin/randbyte?nbytes={0}&format=f'.format(self.default_length), timeout=10)
        self.cache = response.content

        print('Received ', len(self.cache), ' bytes')

        result = self.cache[:length]

        self.cache_index = length

        return result

generator = RandomOrg()

keypair = RSA.generate(1024, generator.generate)

print('Generated RSA keypair.')

private_key = keypair.exportKey()
public_key = keypair.publickey().exportKey()

f = open('private.pem', 'wb')
f.write(private_key)
f.close()

f = open('public.pem', 'wb')
f.write(public_key)
f.close()
