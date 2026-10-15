class MyHashMap:
    """Taula de hash amb UNA SOLA parella per posició (versió de l'escalfament).

    Cada posició de self._table és None o una parella [clau, valor].
    Si dues claus van a la mateixa posició, put() llança KeyError (col·lisió).
    """

    def __init__(self, cap=13):
        self._table = cap * [None]
        self._n = 0

    def _hash_function(self, key):
        return key % len(self._table)

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        self._bucket_put(j, key, value)
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)

    def get(self, key: int) -> int:
        j = self._hash_function(key)
        return self._bucket_get(j, key)

    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        self._bucket_remove(j, key)

    def _bucket_put(self, j,key,value):
        if self._table[j] is None:
            self._table[j] = [[key, value]]
            self._n += 1
        
        elif self._table[j] is not None:
            existeix = False
            for parella in self._table[j]:
                if parella[0] == key:
                    parella[1] = value
                    existeix = True
            if not existeix:
                        self._table[j].append([key, value])
                        self._n +=1

    def _bucket_get(self, j, key):
        if self._table[j] is not None:
            for parella in self._table[j]:
                if parella[0] == key:
                    return parella[1]
            return -1
        return -1

    def _bucket_remove(self, j, key):
        if self._table[j] is not None:
            for parella in self._table[j]:
                if parella[0] == key:
                    self._table[j].remove(parella)
                    self._n -=1

    def _resize(self, cap):
        antiga = self._table
        self._table = cap * [None]
        self._n = 0

        for pos in antiga:
            if pos is not None:
                for key, value in pos:
                    j = self._hash_function(key)
                    self._bucket_put(j, key, value)
    
    def __len__(self):
        return self._n


