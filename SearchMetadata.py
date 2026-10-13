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
        return f"SearchMetadata: {len(self.image_data)} imatges registrades"

    def prompt(self, sub: str) -> list:
        # Retorna els UUID de les imatges el prompt de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_prompt(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def model(self, sub: str) -> list:
        # Retorna els UUID de les imatges el model de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_model(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def seed(self, sub: str) -> list:
        # Retorna els UUID de les imatges el seed de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_seed(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def cfg_scale(self, sub: str) -> list:
        # Retorna els UUID de les imatges el cfg_scale de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_cfg_scale(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def steps(self, sub: str) -> list:
        # Retorna els UUID de les imatges el steps de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_steps(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def sampler(self, sub: str) -> list:
        # Retorna els UUID de les imatges el sampler de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_sampler(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def date(self, sub: str) -> list:
        # Retorna els UUID de les imatges el created_date de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_created_date(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def generated(self, sub: str) -> list:
        # Retorna els UUID de les imatges el generated de les quals conté la subcadena
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_generated(uuid)
            if valor is not None and valor !="None" and valor.find(sub) != -1:
                resultat.append(uuid)
        return resultat

    def dimensions(self, width: int, height: int) -> list:
        # Retorna els UUID de les imatges amb les dimensions especificades
        resultat = []
        for uuid in self.image_data._imatges:
            valor = self.image_data.get_dimensions(uuid)
            if valor is not None and valor !="None":
                if valor == (width, height):
                    resultat.append(uuid)
        return resultat

    def and_operator(self, list1: list, list2: list) -> list:
        
        list1_set = set(list1)
        list2_set = set(list2)
        return list(list1_set & list2_set)

    def or_operator(self, list1: list, list2: list) -> list:
        list1_set = set(list1)
        list2_set = set(list2)
        return list(list1_set | list2_set)

