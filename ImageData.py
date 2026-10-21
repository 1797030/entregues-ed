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
import cfg
from PIL import Image

class ImageData ():

    CAMPS = ['prompt', 'seed', 'cfg_scale', 'steps',
             'sampler', 'model', 'generated', 'created_date']


    def __init__(self):
        self._imatges = {}

    def __len__(self) -> int:
            return len(self._imatges)
    
    def __str__(self) -> str:
        return f"ImageData: {len(self)} imatges registrades"

    def __iter__(self):
        return iter(self._imatges)

    def __contains__(self, uuid) -> bool:
        if uuid is None:
            return False
        return str(uuid) in self._imatges

    def __getitem__(self, uuid):
        if uuid is None:
            return None
        return self._imatges.get(str(uuid))

    @staticmethod
    def _find_file(file: str) -> str:
        if not file or not isinstance(file, str):
            return None
        candidates = [
            file,
            os.path.join(cfg.ROOT_DIR, file),
            os.path.join(cfg.get_root(), file),
            os.path.join("generated_images", file),
            os.path.join(os.path.dirname(__file__), "..", "..", "generated_images", file),
            os.path.join(os.path.dirname(__file__), "..", "generated_images", file),
        ]
        norm = file.replace("\\", "/")
        if "generated_images/" in norm:
            sub = norm.split("generated_images/")[-1]
            candidates.extend([
                sub,
                os.path.join(cfg.ROOT_DIR, sub),
                os.path.join(cfg.get_root(), sub),
                os.path.join("generated_images", sub),
            ])
        for c in candidates:
            if os.path.isfile(c):
                return c
        return None

    def add_image(self, uuid: str, file: str) -> None:
        if not uuid or not file:
            return

        # No afegim imatges falses (arxius inexistents)
        if self._find_file(file) is None:
            return

        uuid_str = str(uuid)
        self._imatges[uuid_str] = {
            "file": file,
            "dimensions": None,
            "metadata": None
        }

    def remove_image(self, uuid: str) -> None:
        if uuid is None:
            return
        uuid_str = str(uuid)
        if uuid_str in self._imatges:
            del self._imatges[uuid_str]

    def load_metadata(self, uuid: str) -> None:
        if uuid is None:
            return
        uuid_str = str(uuid)
        if uuid_str not in self._imatges:
            return

        entrada = self._imatges[uuid_str]
        path = self._find_file(entrada['file'])

        # Reiniciem
        entrada['dimensions'] = (None, None)
        entrada['metadata'] = {camp: "None" for camp in self.CAMPS}

        if path is None or not os.path.isfile(path):
            return

        try:
            with Image.open(path) as img:
                entrada['dimensions'] = (img.width, img.height)
                text = getattr(img, "text", {})   # text chunks del PNG
        except Exception:
            return

        meta = {str(k).lower(): str(v) for k, v in text.items()}
        entrada['metadata'] = {camp: meta.get(camp, "None") for camp in self.CAMPS}

    def get_filename(self, uuid: str) -> str:
        if uuid is None:
            return None
        uuid_str = str(uuid)
        if uuid_str not in self._imatges:
            return None
        return self._imatges[uuid_str]['file']

    def get_file(self, uuid: str) -> str:
        return self.get_filename(uuid)
    
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
        if uuid is None:
            return None
        uuid_str = str(uuid)
        if uuid_str not in self._imatges or self._imatges[uuid_str]['dimensions'] is None:
            return None
        return self._imatges[uuid_str]['dimensions']

    def _get_field(self, uuid: str, field: str) -> str:
        if uuid is None:
            return None
        uuid_str = str(uuid)
        if uuid_str not in self._imatges:
            return None
        if self._imatges[uuid_str]['metadata'] is None:
            return None
        val = self._imatges[uuid_str]['metadata'].get(field, "None")
        return str(val) if val is not None else "None"

    