class HashTable:
    def __init__(self, size):
        self.load_factor = 0.7
        self.size = size
        self.table = [None] * size
        self.num_elements = 0

    def _hash(self, key):
        if type(key) is str:
            return sum([ord(c) for c in key]) % self.size
        return key % self.size

    def _probe(self, index, i):
        return (index + i**2) % self.size
    
    def _rehash(self):
        old_table = self.table
        self.size *= 2
        self.table = [None] * self.size
        self.num_elements = 0
        for item in old_table:
            if item is not None:
                self.insert(item[0], item[1])

    def insert(self, key, value):
        if self.num_elements / self.size > self.load_factor:
            self._rehash()

        index = self._hash(key)
        aux = index
        i = 0
        while i < self.size:
            if self.table[index] is None:
                self.table[index] = (key, value)
                self.num_elements += 1
                return
            else:
                i += 1
                index = self._probe(aux, i)
        raise Exception("Hash table is full")

    def get(self, key):
        index = self._hash(key)
        aux = index
        i = 0
        while i < self.size:
            if self.table[index] is None:
                return None  # Key not found
            elif self.table[index][0] == key:
                return self.table[index][1]  # Return the value of the key
            else:
                i += 1
                index = self._probe(aux, i)
        return None  # Key not found


    def display(self):
        for i, item in enumerate(self.table):
            if item is not None:
                print(f"Slot {i}: {item[0]} => {item[1]}")
            else:
                print(f"Slot {i}: Empty")
