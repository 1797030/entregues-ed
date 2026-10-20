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
import cfg

class ImageFiles():
    def __init__(self) -> None: 
        self._darrers_afegits = set()
        self._darrers_eliminats = set()
        self._arxius_actuals = set()

    def reload_fs(self, path: str) -> None:
        collection_root = os.path.realpath(cfg.get_root())
        root = os.path.realpath(path) if path else collection_root
        resultat = set()
        if os.path.isdir(root):
            for directory, _, filenames in os.walk(root):
                for filename in filenames:
                    if filename.lower().endswith(".png"):
                        full_path = os.path.join(directory, filename)
                        try:
                            relative = os.path.relpath(full_path, collection_root)
                        except ValueError:
                            relative = os.path.relpath(full_path, root)
                        resultat.add(relative.replace(os.sep, "/"))
        
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


                
        


