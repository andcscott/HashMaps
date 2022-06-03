# Name: Andrew Scott
# OSU Email: scottand@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 2022-06-03
# Description: HashMap implementation using Open Addressing with Quadratic
#              Probing


from a6_include import DynamicArray, HashEntry, hash_function_1, hash_function_2


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ""
        for i in range(self._buckets.length()):
            out += str(i) + ": " + str(self._buckets[i]) + "\n"
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """Adds (or updates) a key/value pair to the hash map

        Parameters
        ----------
        key : str
            Identifier for the given value
        value : object
            Value to add, or update if the key is already present
        """

        # resize if necessary
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        # calculate proper index and add/update HashEntry
        hash = self._hash_function(key)
        initial_index = hash % self._capacity
        is_placed = False
        quadratic_factor = 0
        index = initial_index
        while not is_placed:
            if self._buckets[index] is None:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1
                is_placed = True
            elif self._buckets[index].is_tombstone:
                self._buckets[index].key = key
                self._buckets[index].value = value
                self._buckets[index].is_tombstone = False
                self._size += 1
                is_placed = True
            elif self._buckets[index].key == key:
                self._buckets[index].value = value
                is_placed = True
            else:
                quadratic_factor += 1
                index = (initial_index + quadratic_factor**2) % self._capacity

    def table_load(self) -> float:
        """Get the current hash table load factor

        Returns
        -------
        float
            The load factor
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """Gets the number of empty buckets in the hash table

        Returns
        -------
        int
            Number of empty buckets
        """

        count = 0
        for i in range(self._buckets.length()):
            entry = self._buckets[i]
            if entry is None or entry.is_tombstone:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the hash table

        All existing key/value pairs remain and are rehashed. Does nothing if
        the new capacity is less than 1.

        Parameters
        ----------
        new_capacity : int
            New capacity for the hash table
        """

        # immediately return if new_capacity is invalid
        if new_capacity < 1 or new_capacity < self._size:
            return
        # create new hash table
        new_table = DynamicArray()
        old_table = self._buckets
        for i in range(new_capacity):
            new_table.append(None)
        self._buckets = new_table
        self._size = 0
        self._capacity = new_capacity
        for i in range(old_table.length()):
            if old_table[i] is not None and not old_table[i].is_tombstone:
                self.put(old_table[i].key, old_table[i].value)

    def get(self, key: str) -> object:
        """Get the value associated with a key

        Parameters
        ----------
        key : str
            The key to look up in the hash map

        Returns
        -------
        object
            The value associated with the key if it exists, otherwise None
        """

        hash = self._hash_function(key)
        initial_index = hash % self._capacity
        index = initial_index
        quadratic_factor = 0
        while self._buckets[index] is not None:
            if (
                self._buckets[index].key == key
                and not self._buckets[index].is_tombstone
            ):
                return self._buckets[index].value
            else:
                quadratic_factor += 1
                index = (initial_index + quadratic_factor**2) % self._capacity
        return None

    def contains_key(self, key: str) -> bool:
        """Checks if a given key is in the hash map

        Parameters
        ----------
        key : str
            Key to look up in the hash map

        Returns
        -------
        bool
            True if the key is in the hash map, otherwise False
        """

        hash = self._hash_function(key)
        initial_index = hash % self._capacity
        index = initial_index
        quadratic_factor = 0
        while self._buckets[index] is not None:
            if self._buckets[index].key == key:
                return True
            else:
                quadratic_factor += 1
                index = (initial_index + quadratic_factor**2) % self._capacity
        return False

    def remove(self, key: str) -> None:
        """Removes a key/value pair from the hash map

        Parameters
        ----------
        key : str
            Key to look up in the hash map
        """

        hash = self._hash_function(key)
        initial_index = hash % self._capacity
        index = initial_index
        quadratic_factor = 0
        while self._buckets[index] is not None:
            if (
                self._buckets[index].key == key
                and not self._buckets[index].is_tombstone
            ):
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return
            else:
                quadratic_factor += 1
                index = (initial_index + quadratic_factor**2) % self._capacity

    def clear(self) -> None:
        """Clear the contents of the hash map without changing its capacity"""

        self._buckets = DynamicArray()
        self._size = 0
        for i in range(self._capacity):
            self._buckets.append(None)

    def get_keys(self) -> DynamicArray:
        """Get an array that contains all the keys in the hash map

        Returns
        -------
        DynamicArray
            Array containing the hash maps keys
        """

        keys = DynamicArray()
        for i in range(self._capacity):
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                keys.append(self._buckets[i].key)
        return keys


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put("str" + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put("str" + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put("key1", 10)
    print(m.table_load())
    m.put("key2", 20)
    print(m.table_load())
    m.put("key1", 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put("key" + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key1", 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key2", 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key1", 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put("key4", 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put("key" + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() >= 0.5:
            print(
                "Check that capacity gets updated during resize(); "
                "don't wait until the next put()"
            )

        m.put("some key", "some value")
        result = m.contains_key("some key")
        m.remove("some key")

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(
            capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2)
        )

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get("key"))
    m.put("key1", 10)
    print(m.get("key1"))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key("key1"))
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key3", 30)
    print(m.contains_key("key1"))
    print(m.contains_key("key4"))
    print(m.contains_key("key2"))
    print(m.contains_key("key3"))
    m.remove("key3")
    print(m.contains_key("key3"))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get("key1"))
    m.put("key1", 10)
    print(m.get("key1"))
    m.remove("key1")
    print(m.get("key1"))
    m.remove("key4")

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key1", 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity())
    m.put("key2", 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put("200", "2000")
    m.remove("100")
    m.resize_table(2)
    print(m.get_keys())
