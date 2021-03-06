# Author: Andrew Scott
# Description: HashMap implementation using Separate Chaining for collision
#              resolution

from hm_include import (
    DynamicArray,
    LinkedList,
    SLNode,
    hash_function_1,
    hash_function_2,
)


class HashMap:
    """
    Hash map that uses separate chaining for colision resolution

    Parameters
    ----------
    capacity : int
        Initial capacity for the hash map
    function : function
        Hash function to use
    """

    def __init__(self, capacity: int, function) -> None:
        """Constructor for the HashMap class"""
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """Override string method to provide more readable output

        Returns
        -------
        str
            Hash map in human readable form
        """

        out = ""
        for i in range(self._buckets.length()):
            out += str(i) + ": " + str(self._buckets[i]) + "\n"
        return out

    def get_size(self) -> int:
        """Get the map size

        Returns
        -------
        int
            Size of the hash map
        """

        return self._size

    def get_capacity(self) -> int:
        """Get the map capacity

        Returns
        -------
        int
            Capacity of the hash map
        """

        return self._capacity

    def put(self, key: str, value: object) -> None:
        """Adds (or updates) a key/value pair to the hash map

        Parameters
        ----------
        key : str
            Identifier for the given value
        value : object
            Value to add, or update if the key is already present
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        node = self._buckets[index].contains(key)
        if node is None:
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            node.value = value

    def find_mode_put(self, key: str, value: object) -> None:
        """Alternative put() method to help find_mode() track frequency

        Parameters
        ----------
        key : str
            Identifier for the given value
        value : object
            Value to add, or update if the key is already present
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        node = self._buckets[index].contains(key)
        if node is None:
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            node.value = node.value + value

    def empty_buckets(self) -> int:
        """Gets the number of empty buckets in the hash table

        Returns
        -------
        int
            Number of empty buckets
        """

        count = 0
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """Get the current hash table load factor

        Returns
        -------
        float
            The load factor
        """

        return self._size / self._capacity

    def clear(self) -> None:
        """Clear the contents of the hash map without changing its capacity"""

        for i in range(self._capacity):
            if self._buckets[i].length() != 0:
                self._buckets[i] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """Changes the capacity of the hash table

        All existing key/value pairs remain and are rehashed. Does nothing if
        the new capacity is less than 1.

        Parameters
        ----------
        new_capacity : int
            New capacity for the hash table
        """

        # immediately return if new_capacity is less than 1
        if new_capacity < 1:
            return
        # create new hash table if new_capacity is 1 or greater
        new_table = DynamicArray()
        for i in range(new_capacity):
            new_table.append(LinkedList())
        # rehash and move values from current to new hash table
        for i in range(self._capacity):
            linked_list = self._buckets[i]
            if linked_list.length() != 0:
                for node in linked_list:
                    hash = self._hash_function(node.key)
                    index = hash % new_capacity
                    new_table[index].insert(node.key, node.value)
        # assign the new table and capacity to the existing HashMap object
        self._buckets = new_table
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """Get the value associated with the given key

        Parameters
        ----------
        key : str
            Key to look up in the hash map

        Returns
        -------
        object
            The value associated with the key, or None if the key does not exist
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        node = self._buckets[index].contains(key)
        if node is None:
            return node
        return node.value

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

        # immediately return if the hash map is empty
        if self._size == 0:
            return False
        # proceed to check for key in non-empty hash map
        hash = self._hash_function(key)
        index = hash % self._capacity
        node = self._buckets[index].contains(key)
        if node is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """Removes a key/value pair from the hash map

        Parameters
        ----------
        key : str
            Key to look up in the hash map
        """

        hash = self._hash_function(key)
        index = hash % self._capacity
        is_removed = self._buckets[index].remove(key)
        if is_removed:
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """Get an array that contains all the keys in the hash map

        Returns
        -------
        DynamicArray
            Array containing the hash maps keys
        """

        keys = DynamicArray()
        for i in range(self._capacity):
            linked_list = self._buckets[i]
            for node in linked_list:
                keys.append(node.key)
        return keys


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """Get the mode(s) and their frequency from a dynamic array

    If there is more than one value that has the highest frequency all values at
    that frequency will be included. The dynamic array must contain at least 1
    element, and all elements must be strings.

    Parameters
    ----------
    da : DynamicArray
        The dynamic array for which mode and frequency is needed

    Returns
    -------
    (DynamicArray, int) : tuple
        Dynamic array with the mode(s), Integer representing highest frequency
    """

    mode_arr = DynamicArray()
    if da.length() == 1:
        mode_arr.append(da[0])
        return mode_arr, 1

    map = HashMap(da.length() // 3, hash_function_1)
    for i in range(da.length()):
        map.find_mode_put(da[i], 1)

    keys = map.get_keys()
    max_val = 1
    for i in range(keys.length()):
        value = map.get(keys[i])
        if value > max_val:
            max_val = value
            mode_arr = DynamicArray()
            mode_arr.append(keys[i])
        elif value == max_val:
            mode_arr.append(keys[i])

    return mode_arr, max_val

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

    print("\n empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put("key" + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\n table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put("key1", 10)
    print(m.table_load())
    m.put("key2", 20)
    print(m.table_load())
    m.put("key1", 30)
    print(m.table_load())

    print("\n table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put("key" + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\n clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put("key1", 10)
    m.put("key2", 20)
    m.put("key1", 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\n clear example 2")
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

    print("\n resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put("key1", 10)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get("key1"), m.contains_key("key1"))

    print("\n resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put("some key", "some value")
        result = m.contains_key("some key")
        m.remove("some key")

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(
            capacity,
            result,
            m.get_size(),
            m.get_capacity(),
            round(m.table_load(), 2),
        )

    print("\n get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get("key"))
    m.put("key1", 10)
    print(m.get("key1"))

    print("\n get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\n contains_key example 1")
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

    print("\n contains_key example 2")
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

    print("\n remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get("key1"))
    m.put("key1", 10)
    print(m.get("key1"))
    m.remove("key1")
    print(m.get("key1"))
    m.remove("key4")

    print("\n get_keys example 1")
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

    print("\n find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\n find_mode example 2")
    print("-----------------------------")
    test_cases = (
        [
            "Arch",
            "Manjaro",
            "Manjaro",
            "Mint",
            "Mint",
            "Mint",
            "Ubuntu",
            "Ubuntu",
            "Ubuntu",
            "Ubuntu",
        ],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"],
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
