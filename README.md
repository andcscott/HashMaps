# HashMaps

These two hash map implementations feature open addressing with quadratic probing
and separate chaining to handle collisions. The a6\_include module provides the
underlying data structures, and two hash functions.

Both implementations use the included DynamicArray class for the underlying hash table, 
however hash\_map\_sc.py uses a singly linked list for each bucket while hash\_map\_oa.py 
uses a HashEntry object. Additionally, hash\_map\_sc.py includes a seperate function, 
find\_mode(), that provides a mechanism for finding the value that occurs most
frequently in the hash map and how many times it occurs with an O(n) time complexity.
