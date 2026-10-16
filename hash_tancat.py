# Estats d'una posició de la taula (hash tancat). NO canvieu aquests valors.
LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    """Taula de hash amb UNA SOLA parella per posició (versió de l'escalfament).

    Cada posició de self._table és None o una parella [clau, valor].
    Si dues claus van a la mateixa posició, put() llança KeyError (col·lisió).
    """

    def __init__(self, cap=13):
        self._table = cap * [[None, None, LLIURE]]   # m posicions, inicialment buides
        self._n = 0                  # nombre de claus desades

    def _hash_function(self, key):
        return key % len(self._table)          # h(x) = x % m

    def put(self, key: int, value: int) -> None:
        j = self._hash_function(key)
        if self._table[j][0] == key:
            self._table[j][1] = value

        if self._table[j][2] == LLIURE:
            self._table[j] = [key, value, OCUPAT]
            self._n +=1

        else:
            index_esborrat = False
            idx = None
            i = 0
            final = False

            while final == False:
                j2 = self._hash_function(j+i)
                if self._table[j2][2] == ESBORRAT and not index_esborrat:
                    idx = j2
                    index_esborrat = True
                elif self._table[j2][2] == LLIURE:
                    if index_esborrat:
                        self._table[idx] = [key, value, OCUPAT]
                        self._n +=1
                        final = True
                    else:
                        self._table[j2] = [key, value, OCUPAT]
                        self._n +=1
                        final = True
                i +=1
        if self._n > len(self._table) // 2:
            self._resize(2 * len(self._table) - 1)


    def get(self, key: int) -> int:
        j = self._hash_function(key)
        if self._table[j] is not None and self._table[j][0] == key:
            return self._table[j][1]
        else:
            i = 1
            final = False
            while final == False:
                j2 = self._hash_function(j+i)
                if self._table[j2] is not None and self._table[j2][0] == key:
                            return self._table[j2][1]
                elif j == j2:
                    final = True
                i +=1
            return -1


    def remove(self, key: int) -> None:
        j = self._hash_function(key)
        if self._table[j][0] == key:
            self._table[j] = [None, None, ESBORRAT]
            self._n -= 1
        else:
            final = False
            i = 1
            while final == False:
                j2 = self._hash_function(j+i)
                if self._table[j2] is not None and self._table[j2][0] == key:
                    self._table[j2] = [None, None, ESBORRAT]
                    self._n -= 1
                    final = True
                elif j == j2:
                    final = True

    def _resize(self, cap):
        antiga = self._table
        self._table = cap * [[None, None, LLIURE]]
        self._n = 0

        for pos in antiga:
                if pos[2] == OCUPAT:
                    self.put(pos[0], pos[1])
                
    def __len__(self):
        return self._n

hm = MyHashMap()
hm.put(40, 7)
hm.put(14, 3)        # h(14) = h(40) = 1: va a la posició 2
hm.put(27, 1)        # h(27) = 1: va a la posició 3
print(hm._table[1:4])       # → [[40, 7, 'O'], [14, 3, 'O'], [27, 1, 'O']]
hm.remove(14)
print(hm._table[2])         # → [None, None, 'B']
print(hm.get(27))           # → 1   (salta la posició ESBORRAT 2)
print(hm.get(14))           # → -1
hm.put(53, 9)        # h(53) = 1: reutilitza la posició ESBORRAT 2
print(hm._table[2])         # → [53, 9, 'O']
print(len(hm))              # → 3


hm = MyHashMap()
for k in [23, 45, 16, 26, 40, 14, 5, 12, 9, 25]:
    hm.put(k, 10 * k)
print(len(hm._table))       # → 25  (ha redimensionat en inserir la 7a clau)
print(hm.get(25))           # → 250