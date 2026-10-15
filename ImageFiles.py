# -*- coding: utf-8 -*-
"""
ImageFiles.py : ** REQUIRED ** El vostre codi de la classe ImageFiles.

Aquesta classe s'encarrega de gestionar el llistat d'arxius PNG dins la col·lecció d'imatges.

Funcionalitat:
    - Recórrer el filesystem a partir de ROOT_DIR per trobar tots els arxius PNG
    - Mantenir una representació en memòria dels arxius presents
    - Detectar quins arxius s'han afegit o eliminat des de l'última lectura

Mètodes a implementar:
    - reload_fs(path: str) -> None
        Recorre el directori especificat i actualitza la llista d'arxius PNG.
        Detecta els arxius nous i els que s'han eliminat.

    - files_added() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han afegit des de l'última crida a reload_fs().

    - files_removed() -> list
        Retorna una llista (de strings) amb els paths relatius dels arxius
        que s'han eliminat des de l'última crida a reload_fs().

Notes:
    - Els paths han de ser sempre relatius a ROOT_DIR
    - Només considereu arxius amb extensió .png (case-insensitive)
    - Heu de recórrer tots els subdirectoris recursivament
"""
from typing import List
import os

class ImageFiles():
    def __init__(self) -> None: 
        self._darrers_afegits = set()
        self._darrers_eliminats = set()
        self._arxius_actuals = set()

    def reload_fs(self, path: str) -> None:
        resultat = set()
        for carpeta_actual, subcarpetes, arxius in os.walk(path): #os.walr permet la cerca recursiva, però no se si ho he d'implementar jo des de 0
            for arxiu in arxius:
                if arxiu.lower().endswith(".png"):
                    path_complet = os.path.join(carpeta_actual, arxiu)

                    path_relatiu = os.path.relpath(
                        path_complet,
                        path
                    )

                    
                    path_relatiu = path_relatiu.replace(os.sep, "/")

                    resultat.add(path_relatiu)
        
        #El fet d'utilitzar sets ens permet fer aquestes operacions
        self._darrers_afegits = resultat - self._arxius_actuals
        self._darrers_eliminats = self._arxius_actuals - resultat
        self._arxius_actuals = resultat


    def files_added(self) -> List:
        return list(self._darrers_afegits)

    def files_removed(self) -> List:
        return list(self._darrers_eliminats)

    def __str__(self):
        return str(self._arxius_actuals)


                
        


