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

    @staticmethod
    def _configured_root() -> str:
        """Resol l'arrel encara que ROOT_DIR sigui relativa."""
        root = cfg.ROOT_DIR
        if os.path.isabs(root):
            return os.path.realpath(root)

        # cfg.py pot definir ROOT_DIR respecte del directori d'execució.
        # Si aquesta resolució no existeix, provem respecte de cfg.py.
        from_cwd = os.path.realpath(root)
        cfg_file = getattr(cfg, "__file__", None)
        if cfg_file:
            from_cfg = os.path.realpath(
                os.path.join(os.path.dirname(os.path.abspath(cfg_file)), root)
            )
            if os.path.isdir(from_cfg):
                return from_cfg
        return from_cwd

    def reload_fs(self, path: str) -> None:
        if not os.path.isdir(path):
            configured_root = self._configured_root()
            if os.path.isdir(configured_root):
                path = configured_root

        resultat = set()
        for carpeta_actual, subcarpetes, arxius in os.walk(path): #os.walr permet la cerca recursiva, però no se si ho he d'implementar jo des de 0
            for arxiu in arxius:
                if arxiu.lower().endswith(".png"):
                    path_complet = os.path.join(carpeta_actual, arxiu)


                    root = self._configured_root()
                    path_relatiu = os.path.relpath(path_complet, root)

                    
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


                
        


