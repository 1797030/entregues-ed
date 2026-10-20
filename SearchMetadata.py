# -*- coding: utf-8 -*-
"""
SearchMetadata.py : ** REQUIRED ** El vostre codi de la classe SearchMetadata.

Aquesta classe s'encarrega de cercar imatges segons criteris basats en metadades.

Funcionalitat:
    - Cercar imatges que continguin una subcadena en les seves metadades
    - Combinar resultats de cerques amb operadors lògics (AND, OR)

Mètodes a implementar:
    - prompt(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Prompt.

    - model(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Model.

    - seed(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Seed.

    - cfg_scale(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp CFG_Scale.

    - steps(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Steps.

    - sampler(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Sampler.

    - date(sub: str) -> list
        Retorna una llista d'UUID de les imatges que contenen 'sub'
        en el camp Created_Date.

    - and_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en AMBDUES llistes.
        (Intersecció de conjunts)

    - or_operator(list1: list, list2: list) -> list
        Retorna una llista amb els UUID que apareixen en QUALSEVOL de
        les dues llistes, sense duplicats.
        (Unió de conjunts)

Notes:
    - Les cerques són case-sensitive (distingeixen majúscules/minúscules)
    - Utilitzeu str.find() per cercar subcadenes
    - Les llistes retornades poden estar buides
    - Els operadors lògics NO modifiquen les llistes originals
    - Aquests mètodes NO retornen objectes Gallery, sinó llistes simples
"""


import cfg
class SearchMetadata:
    def __init__(self, image_data):
        self.image_data = image_data

    def __str__(self):
        n = len(self.image_data) if self.image_data is not None else 0
        return f"SearchMetadata: {n} imatges registrades"

    def _cercar_subcadena(self, getter_func, sub) -> list:
        # Retorna una llista buida si el valor de cerca és None
        if sub is None:
            return []
        if not isinstance(sub, str):
            try:
                sub = str(sub)
            except Exception:
                return []

        if not self.image_data or not hasattr(self.image_data, '_imatges'):
            return []

        resultat = []
        for uuid in self.image_data._imatges:
            valor = getter_func(uuid)
            if valor is not None and valor != "None":
                if not isinstance(valor, str):
                    valor = str(valor)
                if valor.find(sub) != -1:
                    resultat.append(uuid)
        return resultat

    def prompt(self, sub: str) -> list:
        # Retorna els UUID de les imatges el prompt de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_prompt, sub)

    def model(self, sub: str) -> list:
        # Retorna els UUID de les imatges el model de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_model, sub)

    def seed(self, sub: str) -> list:
        # Retorna els UUID de les imatges el seed de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_seed, sub)

    def cfg_scale(self, sub: str) -> list:
        # Retorna els UUID de les imatges el cfg_scale de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_cfg_scale, sub)

    def steps(self, sub: str) -> list:
        # Retorna els UUID de les imatges el steps de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_steps, sub)

    def sampler(self, sub: str) -> list:
        # Retorna els UUID de les imatges el sampler de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_sampler, sub)

    def date(self, sub: str) -> list:
        # Retorna els UUID de les imatges el created_date de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_created_date, sub)

    def generated(self, sub: str) -> list:
        # Retorna els UUID de les imatges el generated de les quals conté la subcadena
        return self._cercar_subcadena(self.image_data.get_generated, sub)

    def dimensions(self, width: int, height: int) -> list:
        # Retorna els UUID de les imatges amb les dimensions especificades
        if width is None or height is None:
            return []
        try:
            w, h = int(width), int(height)
            if w <= 0 or h <= 0:
                return []
        except (ValueError, TypeError):
            return []

        if not self.image_data or not hasattr(self.image_data, '_imatges'):
            return []

        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_dimensions(uuid)
            if valor is not None and valor != "None" and valor == (w, h):
                resultat.append(uuid)
        return resultat

    def and_operator(self, list1: list, list2: list) -> list:
        if list1 is None or list2 is None:
            return []
        try:
            list1_set = set(list1)
            list2_set = set(list2)
            return list(list1_set & list2_set)
        except Exception:
            return []

    def or_operator(self, list1: list, list2: list) -> list:
        l1 = list1 if list1 is not None else []
        l2 = list2 if list2 is not None else []
        try:
            list1_set = set(l1)
            list2_set = set(l2)
            return list(list1_set | list2_set)
        except Exception:
            return []
