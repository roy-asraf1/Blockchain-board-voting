
# create hash table for the stocks of all the members of thr directors
class Directors:

    # Create empty bucket list of given size with all the stocks of the company
    # Constructor
    def __init__(self, size, stocks_company):
        self.size = size
        self.hash_table = self.create_buckets()
        self.stocks_company = stocks_company

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    # Insert the numbers of one person into hash map
    def set_stocks(self, id, stocks):

        # Get the index from the key
        # using hash function
        hashed_id = hash(id) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_id]

        found_id = False
        for index, record in enumerate(bucket):
            record_id, record_stocks = record

            # check if the bucket has same id as
            # the id to be inserted
            if record_id == id:
                found_id = True
                break

        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_id:
            bucket[index] = (id, stocks)
        else:
            bucket.append((id, stocks))

    # Return searched value with specific key
    def get_stocks(self, id):

        # Get the index from the key using
        # hash function
        hashed_key = hash(id) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_stocks = record

            # check if the bucket has same id as
            # the id being searched
            if record_key == id:
                found_key = True
                break

        # If the bucket has same key as the id being searched,
        # Return the stocks found
        # Otherwise indicate there was no record found
        if found_key:
            return record_stocks
        else:
            return "No record found"

    # Remove a stocks with specific id
    def delete_stocks(self, stocks):

        # Get the index from the id using
        # hash function
        hashed_id = hash(id) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_id]

        found_id = False
        for index, record in enumerate(bucket):
            record_id, record_stocks = record

            # check if the bucket has same id as the key to be deleted
            if record_id == id:
                found_id = True
                break
        if found_id:
            bucket.pop(index)
        return

    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)


hash_table = Directors(10, 80000)

# insert some values
hash_table.set_stocks('302211958', '40000')
print(hash_table)
print()

hash_table.set_stocks('302211966', '40000')
print(hash_table)
print()

# search/access a record with key
print(hash_table.get_stocks('302211958'))
print()

# delete or remove a value
hash_table.delete_stocks('302211966')
print(hash_table)
