# -*- coding: utf-8 -*-
"""
ImageViewer.py : ** REQUIRED ** El vostre codi de la classe ImageViewer.

Aquesta classe s'encarrega de visualitzar imatges i mostrar les seves metadades.

Funcionalitat:
    - Imprimir per pantalla les metadades d'una imatge
    - Mostrar la imatge en pantalla
    - Combinar ambdues accions segons la configuració

Mètodes a implementar:
    - print_image(uuid: str) -> None
        Imprimeix per pantalla totes les metadades de la imatge identificada
        per l'UUID. Ha de mostrar:
        - Dimensions (width x height)
        - Prompt (truncat si és molt llarg)
        - Model
        - Seed
        - CFG Scale
        - Steps
        - Sampler
        - Generated
        - Created Date
        - UUID
        - Path de l'arxiu

    - show_file(file: str) -> None
        Mostra la imatge especificada utilitzant PIL.
        Aquesta funció NO espera que la imatge es tanqui (asíncrona).

    - show_image(uuid: str, mode: int) -> None
        Combina print_image() i show_file() segons el mode especificat:
        - mode 0: només metadades
        - mode 1: metadades + imatge
        - mode 2: només imatge

        Aquesta funció ha d'esperar que l'usuari tanqui la imatge abans
        de retornar (síncrona). Podeu utilitzar input() per fer una pausa.

Notes:
    - Utilitzeu cfg.DISPLAY_MODE per determinar el comportament per defecte
    - Per mostrar imatges: img.show() de PIL
    - Gestioneu les excepcions si la imatge no es pot mostrar
    - El format de sortida ha de ser llegible i ben organitzat
"""
import os
import cfg
from PIL import Image
from ImageData import ImageData

class ImageViewer ():

    def __init__(self, image_data: ImageData = None) -> None:
        self._image_data = image_data

    def __str__(self) -> str:
        n = len(self._image_data) if self._image_data is not None else 0
        return f"ImageViewer: {n} imatges disponibles (DISPLAY_MODE={cfg.DISPLAY_MODE})"

    def print_image(self, uuid: str) -> None:
        if self._image_data is None:
            print(f"No hi ha cap instància de ImageData.")
            return

        file_path = self._image_data.get_filename(uuid)
        dims = self._image_data.get_dimensions(uuid)
        if dims and dims[0] is not None and dims[1] is not None:
            dims_str = f"{dims[0]}x{dims[1]}"
        else:
            dims_str = "None"

        prompt = self._image_data.get_prompt(uuid)
        if prompt is None:
            prompt = "None"
        prompt_definitiu = prompt[:70] + "..." if len(prompt) > 80 else prompt

        print(f"UUID:         {uuid}")
        print(f"Arxiu:        {file_path}")
        print(f"Dimensions:   {dims_str}")
        print(f"Prompt:       {prompt_definitiu}")
        print(f"Model:        {self._image_data.get_model(uuid)}")
        print(f"Seed:         {self._image_data.get_seed(uuid)}")
        print(f"CFG Scale:    {self._image_data.get_cfg_scale(uuid)}")
        print(f"Steps:        {self._image_data.get_steps(uuid)}")
        print(f"Sampler:      {self._image_data.get_sampler(uuid)}")
        print(f"Generated:    {self._image_data.get_generated(uuid)}")
        print(f"Created Date: {self._image_data.get_created_date(uuid)}")

    def show_file(self, file: str) -> None:
        try:
            if not os.path.isabs(file): # si la ruta no esta completa la completem
                full_path = os.path.join(cfg.ROOT_DIR, file)
            else:
                full_path = file

            if not os.path.isfile(full_path):
                print(f"ERROR: No s'ha trobat el fitxer: {full_path}")
                return

            with Image.open(full_path) as img:
                img.show()

        except Exception as e:
            print(f"ERROR: {e}")

    def show_image(self, uuid: str, mode: int = None) -> None:
        if mode is None:
            mode = cfg.DISPLAY_MODE

        if mode in (0, 1):
            self.print_image(uuid)

        if mode in (1, 2):
            if self._image_data is None:
                print("ERROR: No es pot mostrar la imatge.")
                return

            file_path = self._image_data.get_filename(uuid)
            if file_path == "None" or file_path is None:
                print(f"ERROR: No s'ha trobat cap fitxer associat al UUID {uuid}")
                return

            self.show_file(file_path)
            try:
                input("Prem ENTER per continuar...")
            except (EOFError, KeyboardInterrupt):
                pass