import requests
from Crypto.PublicKey import RSA

# messy globals
random_bytes_cache = b'0'
current_pos = 0
DEFAULT_LENGTH = 4000

# a lil function with the signature RSA.generate wants
def web_random(length):
    global current_pos
    global random_bytes_cache
    global DEFAULT_LENGTH

    # there's unused bytes in the cache, return them
    if random_bytes_cache and current_pos < (len(random_bytes_cache) + length):
        result = random_bytes_cache[current_pos:current_pos + length]
        current_pos += length
        return result

    # new bytes needed
    print('Requesting bytes from random.org...')
    # format=f makes sure data downloaded is binary and not text
    response = requests.get('https://www.random.org/cgi-bin/randbyte?nbytes={0}&format=f'.format(DEFAULT_LENGTH), timeout=10)

    random_bytes_cache = response.content
    current_pos = 0

    print('Received ', len(random_bytes_cache), ' bytes')

    result = random_bytes_cache[current_pos:current_pos + length]
    current_pos += length
    return result


keypair = RSA.generate(1024, web_random)

print('Generated RSA keypair.')

private_key = keypair.exportKey()
public_key = keypair.publickey().exportKey()

f = open('private.pem', 'wb')
f.write(private_key)
f.close()

f = open('public.pem', 'wb')
f.write(public_key)
f.close()
