class MinStack:

    def __init__(self, pila = None):
        if pila == None:
            self._pila = []
            self._llista = []
        else:
            self._pila = list(pila)
            self._llista = []
            for valor in pila:
                if len(self._llista) == 0:
                    self._llista.append(valor)
                else:
                    if self._llista[-1] > valor:
                        self._llista.append(valor)
                    else:
                        self._llista.append(self._llista[-1])

    def push(self, val: int) -> None:
        self._pila.append(val)
        if len(self._llista) == 0 or val <  self._llista[-1]:
            self._llista.append(val)
        else:
            self._llista.append(self._llista[-1])


    def pop(self) -> None:
        self._pila.pop()
        self._llista.pop()

    def top(self) -> int:
        return self._pila[-1]

    def getMin(self) -> int:
        return self._llista[-1]