# -*- coding: utf-8 -*-
"""
Gallery.py : ** REQUIRED ** El vostre codi de la classe Gallery.

Aquesta classe s'encarrega de gestionar galeries d'imatges en format JSON.

Funcionalitat:
    - Llegir galeries des d'arxius JSON
    - Visualitzar totes les imatges d'una galeria
    - Afegir i eliminar imatges de la galeria

Format JSON d'una galeria:
{
  "gallery_name": "Cyberpunk Cities",
  "description": "Collection of futuristic urban landscapes",
  "created_date": "2025-09-30",
  "images": [
    "generated_images/city_001.png",
    "generated_images/city_neon_12.png",
    "generated_images/urban_street_45.png"
  ]
}

Mètodes a implementar:
    - load_file(file: str) -> None
        Llegeix un arxiu JSON amb la definició de la galeria.
        Ha de validar que cada imatge referenciada existeix a la col·lecció.
        Si una imatge no existeix, l'ignora i continua processant.
        Emmagatzema internament els UUID de les imatges vàlides.

    - show() -> None
        Visualitza totes les imatges de la galeria en ordre utilitzant
        ImageViewer.show_image().

    - add_image_at_end(uuid: str) -> None
        Afegeix una imatge al final de la galeria.

    - remove_first_image() -> None
        Elimina la primera imatge de la galeria.

    - remove_last_image() -> None
        Elimina l'última imatge de la galeria.

Notes:
    - Utilitzeu la llibreria json per llegir els arxius
    - Els paths dins el JSON són relatius a ROOT_DIR
    - Cada galeria és un objecte independent (instància de Gallery)
    - Podeu tenir múltiples galeries actives simultàniament
    - Les operacions d'afegir/eliminar són ràpides (no busquen a la llista)
"""

import json
import os
import cfg

class Gallery:
    """Representa una galeria d'imatges carregada desde un fitxer JSON"""
    def __init__(self, image_id=None, image_viewer=None):
        self.images = []
        self.image_id = image_id
        self.image_viewer = image_viewer

    def __len__(self):
        """Retorna el nombre d'imatges vàlides a la galeria."""
        return len(self.images)

    def __str__(self):
        """Retorna una representació llegible de la galeria."""
        return f"Gallery amb {len(self.images)} imatges vàlides."

    def load_file(self, file):
        self.images = []

        if not file or not isinstance(file, str):
            return

        path_fitxer = file
        if not os.path.isabs(path_fitxer) and not os.path.exists(path_fitxer):
            candidat = os.path.join(cfg.ROOT_DIR, path_fitxer)
            if os.path.exists(candidat):
                path_fitxer = candidat

        if not os.path.isfile(path_fitxer):
            return

        try:
            with open(path_fitxer, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError, TypeError):
            return

        root_name = cfg.ROOT_DIR.replace("\\", "/").rstrip("/").split("/")[-1]
        imatges = data.get("images", []) if isinstance(data, dict) else []

        if self.image_id is None:
            return

        for image_path in imatges:
            if not isinstance(image_path, str):
                continue

            path = image_path.replace("\\", "/").lstrip("/")
            prefix = root_name + "/"
            if path.startswith(prefix):
                path = path[len(prefix):]

            uuid = self.image_id.get_uuid(path)
            if uuid is not None:
                self.images.append(uuid)
                
    def show(self):
        """Visualitza els UUID de la galeria en ordre."""
        if self.image_viewer is None:
            return

        for uuid in self.images:
            self.image_viewer.show_image(uuid)

    def add_image_at_end(self, uuid):
        """Afegeix una imatge al final de la galeria."""
        if uuid is not None:
            self.images.append(uuid)

    def remove_first_image(self):
        """Elimina la primera imatge de la galeria."""
        if self.images:
            self.images.pop(0)

    def remove_last_image(self):
        """Elimina l'última imatge de la galeria."""
        if self.images:
            self.images.pop()
            
    
