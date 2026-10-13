# -*- coding: utf-8 -*-
"""
ImageID.py : ** REQUIRED ** El vostre codi de la classe ImageID.

Aquesta classe s'encarrega de generar i gestionar identificadors únics (UUID)
per a cada imatge de la col·lecció.

Funcionalitat:
    - Generar un UUID únic a partir del path canònic d'un arxiu
    - Mantenir un registre dels UUID generats per evitar col·lisions
    - Permetre consultar i eliminar UUID

Mètodes a implementar:
    - generate_uuid(file: str) -> str
        Genera un UUID únic per a l'arxiu especificat.
        Ha de comprovar que el UUID no estigui ja en ús.
        Si hi ha col·lisió (cas extremadament improbable), retorna None i
        mostra un missatge d'error.

    - get_uuid(file: str) -> str
        Retorna el UUID associat a l'arxiu, si ja ha estat generat.
        Si no existeix, retorna None.

    - remove_uuid(uuid: str) -> None
        Elimina el UUID del registre d'identificadors actius.
        Després d'eliminar-lo, aquest UUID es podrà tornar a utilitzar.

Notes:
    - Els UUID han de seguir el format estàndard (128 bits)
    - Podeu utilitzar la funció cfg.get_uuid() com a base
    - Els UUID s'emmagatzemen com a strings
    - Un UUID només es pot generar una vegada (fins que s'elimini)
"""
from cfg import get_uuid
class ImageID():
    def __init__(slef)-> None:
        slef._uuid_generats = set() #Un set permet fer totes les operacions de cerca més ràpidament

    def generate_uuid(self, arxiu: str)-> str:
        uuid = str(get_uuid(arxiu)) #Crea el uuid
        if uuid in self._uuid_generats:
            print("UUID ja existent")
            return None
        else:
            self._uuid_generats.add(uuid)
            return uuid
    
    def get_uuid(self, arxiu: str)-> str: #Tornem a caclular el uuid, si ja el tenim el retornam, així no cal guardar el uuid i l'arxiu associat.
        uuid = str(get_uuid(arxiu))
        if uuid in self._uuid_generats:
            return uuid
        else:
            return None

    def remove_uuid(self, uuid: str)-> None:
        try:
            self._uuid_generats.remove(uuid)
        except KeyError: #Si no es troba el uuid
            print("El UUID no existeix")

    def __len__(self):
        return len(self._uuid_generats)
    def __str__(self):
        return str(self._uuid_generats)



        
        


