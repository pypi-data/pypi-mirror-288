import hashlib
import random
import hmac

# OPRF-related functions
def generate_key():
    return random.getrandbits(256).to_bytes(32, byteorder='big')

def oprf(key, value):
    return hmac.new(key, value.encode(), hashlib.sha256).digest()

def hash_element(element, key):
    return hashlib.sha256(oprf(key, element)).hexdigest()

# Batch processing function
def process_batch(batch, key):
    return {hash_element(elem, key): elem for elem in batch}

# Batched OPRF
def batch_oprf(set_a, set_b, batch_size, server_key):

    # Split sets into batches
    batches_a = [list(set_a)[i:i + batch_size] for i in range(0, len(set_a), batch_size)]
    batches_b = [list(set_b)[i:i + batch_size] for i in range(0, len(set_b), batch_size)]

    # Process batches sequentially
    hashed_a_batches = [process_batch(batch, server_key) for batch in batches_a]
    hashed_b_batches = [process_batch(batch, server_key) for batch in batches_b]

    # Combine all hashed elements
    hashed_a = {k: v for batch in hashed_a_batches for k, v in batch.items()}
    hashed_b = {k: v for batch in hashed_b_batches for k, v in batch.items()}

    # Find the intersection of hashed values
    intersection_hashes = set(hashed_a.keys()).intersection(set(hashed_b.keys()))

    # Map the intersection hashes back to the original elements
    intersection = {hashed_a[h] for h in intersection_hashes}

    return intersection


class PSI:

    @staticmethod
    def get_key():
        # Generate a key for the server
        return generate_key()

    @staticmethod
    def oprf(X, Y, batch_size, server_key):
        # X, Y expects a pandas column from party A & B
        intersection = batch_oprf(set(X), set(Y), batch_size, server_key)
        return intersection
