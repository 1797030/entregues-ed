# -*- coding: utf-8 -*-
"""
ImageData.py : ** REQUIRED ** El vostre codi de la classe ImageData.

Aquesta classe s'encarrega d'emmagatzemar i gestionar les metadades de les
imatges generades per IA.

Funcionalitat:
    - Afegir i eliminar imatges de la col·lecció
    - Llegir les metadades embegudes dins els arxius PNG
    - Proporcionar accés a totes les metadades d'una imatge

Mètodes a implementar:
    - add_image(uuid: str, file: str) -> None
        Crea una entrada per a la imatge amb l'UUID i el path especificats.
        Inicialment les metadades estan buides (no llegides del disc).

    - remove_image(uuid: str) -> None
        Elimina la imatge i totes les seves metadades de la col·lecció.

    - load_metadata(uuid: str) -> None
        Llegeix les metadades embegudes en l'arxiu PNG i les emmagatzema.
        Aquest mètode es pot cridar múltiples vegades (p.ex. si l'arxiu canvia).

    - get_prompt(uuid: str) -> str
        Retorna el prompt utilitzat per generar la imatge.

    - get_model(uuid: str) -> str
        Retorna el model d'IA utilitzat (p.ex. "SD2", "DALL-E", "Midjourney").

    - get_seed(uuid: str) -> str
        Retorna la llavor aleatòria utilitzada en la generació.

    - get_cfg_scale(uuid: str) -> str
        Retorna el CFG Scale (guidance scale) utilitzat.

    - get_steps(uuid: str) -> str
        Retorna el nombre de passos d'iteració del model.

    - get_sampler(uuid: str) -> str
        Retorna l'algorisme de mostreig utilitzat.

    - get_generated(uuid: str) -> str
        Retorna "true" si la imatge està marcada com a generada.

    - get_created_date(uuid: str) -> str
        Retorna la data de creació en format YYYY-MM-DD.

    - get_dimensions(uuid: str) -> tuple
        Retorna una tupla (width, height) amb les dimensions de la imatge.

Notes:
    - Utilitzeu la llibreria PIL/Pillow per llegir metadades:
      img = Image.open(file)
      metadata = img.text
    - Si un camp no existeix, retorneu "None" (string)
    - Les dimensions es llegeixen amb img.width i img.height
    - Tots els camps de metadades es guarden com a strings
"""
import os
from cfg import read_png_metadata, get_png_dimensions

class ImageData ():

    def __init__(self):
        self._imatges = {}

    def __len__(self) -> int:
            return len(self._imatges)
    
    def __str__(self) -> str:
        return f"ImageData: {len(self)} imatges registrades"

    def add_image(self, uuid: str, file: str) -> None:
        self._imatges[uuid] = {
            "file": file,
            "dimensions": (None, None),
            "metadata": {
                'prompt': "None",
                'model': "None",
                'seed': "None",
                'cfg_scale': "None",
                'steps': "None",
                'sampler': "None",
                'generated': "None",
                'created_date': "None"
            }
        }

    def remove_image(self, uuid: str) -> None:
        if uuid not in self._imatges:
            return
        del self._imatges[uuid]

    def load_metadata(self, uuid: str) -> None:
        if uuid not in self._imatges:
            return

        entrada = self._imatges[uuid]
        path = os.path.join(cfg.ROOT_DIR, entrada['file']) #uneix el directori amb la ruta alternativa

        # Reiniciem tot abans de llegir
        entrada['dimensions'] = (None, None)
        camps = ['prompt', 'seed', 'cfg_scale', 'steps', 'sampler', 'model', 'generated', 'created_date']
        entrada['metadata'] = {camp: "None" for camp in camps}
        
        dimensions = get_png_dimensions(path)
        if dimensions:
            entrada['dimensions'] = dimensions

        # Llegir metadades PNG
        meta_1 = read_png_metadata(path)
        if not meta_1:
            return
    
        meta = {str(k).lower(): str(v) for k, v in meta_1.items()} # passem tot a minuscules

        for camp in camps:
            entrada['metadata'][camp] = meta.get(camp, "None")

    def get_filename(self, uuid: str) -> str:
        if uuid in self._imatges:
            return self._imatges[uuid]['file']
        return "None"
    
    def get_prompt(self, uuid: str) -> str:
        return self._get_field(uuid, 'prompt')
    
    def get_model(self, uuid: str) -> str:
            return self._get_field(uuid, 'model')

    def get_seed(self, uuid: str) -> str:
        return self._get_field(uuid, 'seed')
    
    def get_cfg_scale(self, uuid: str) -> str:
        return self._get_field(uuid, 'cfg_scale')

    def get_steps(self, uuid: str) -> str:
        return self._get_field(uuid, 'steps')

    def get_sampler(self, uuid: str) -> str:
        return self._get_field(uuid, 'sampler')

    def get_generated(self, uuid: str) -> str:
        return self._get_field(uuid, 'generated')

    def get_created_date(self, uuid: str) -> str:
        return self._get_field(uuid, 'created_date')

    def get_dimensions(self, uuid: str) -> tuple:
        # Retorna (width, height) amb les dimensions de la imatge.
        if uuid in self._imatges:
            return self._imatges[uuid]['dimensions']
        return (None, None)

    def _get_field(self, uuid: str, field: str) -> str:
        if uuid in self._imatges and field in self._imatges[uuid]['metadata']:
            val = self._imatges[uuid]['metadata'][field]
            return str(val) if val is not None else "None"
        return "None"

    