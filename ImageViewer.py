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
    """Mostra per pantalla les metadades i la imatge d'una imatge registrada.
 
    Estructura de dades interna:
        self._image_data (ImageData): únic atribut de la classe. És una
        referència (no una còpia) a la instància d'ImageData que conté la
        col·lecció. ImageViewer no té cap llista ni diccionari propi:
        quan necessita una dada (path, dimensions, prompt, model...) la
        consulta a ImageData a partir de l'UUID.
 
    Així es evita duplicar les dades i la informació sempre està
    actualitzada. Com que ImageData guarda les imatges en un diccionari,
    cada consulta per UUID és de cost mitjà O(1). Els valors que es
    fan servir dins els mètodes són només variables locals i temporals:
    strings (paths, camps de metadades, prompt truncat) i una tupla
    (width, height) per a les dimensions.
    """
 
    def __init__(self, image_data: ImageData = None) -> None:
        """Associa el visor a la col·lecció d'imatges.
 
        Args:
            image_data (ImageData): Instància amb les metadades de les
                imatges. Si és None, el visor no podrà mostrar res.
        """
        self._image_data = image_data
 
    def __str__(self) -> str:
        """Retorna una descripció amb el nombre d'imatges i el mode actual."""
        # Si no hi ha ImageData associat, comptem 0 imatges
        n = len(self._image_data) if self._image_data is not None else 0
        return f"ImageViewer: {n} imatges disponibles (DISPLAY_MODE={cfg.DISPLAY_MODE})"
 
    def print_image(self, uuid: str) -> None:
        """Imprimeix per pantalla les metadades d'una imatge.
 
        Les dades es consulten a ImageData (memòria), sense llegir l'arxiu
        del disc.
 
        Args:
            uuid (str): Identificador de la imatge.
        """
        # Sense ImageData no hi ha cap dada a mostrar
        if self._image_data is None:
            print(f"No hi ha cap instància de ImageData.")
            return
 
        file_path = self._image_data.get_filename(uuid)
        # Formatem les dimensions com 'AMPLExALÇADA'; si no estan
        # disponibles mostrem 'None'
        dims = self._image_data.get_dimensions(uuid)
        if dims and dims[0] is not None and dims[1] is not None:
            dims_str = f"{dims[0]}x{dims[1]}"
        else:
            dims_str = "None"
 
        # Si el prompt no està disponible, el tractem com a 'None'
        prompt = self._image_data.get_prompt(uuid)
        if prompt is None:
            prompt = "None"
        # Si el prompt supera els 80 caràcters, el truncem a 70 i afegim
        # punts suspensius
        prompt_definitiu = prompt[:70] + "..." if len(prompt) > 80 else prompt
 
        # Sortida formatada, amb les etiquetes alineades en columnes
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
        """Obre la imatge amb el visualitzador del sistema (asíncron).
 
        No espera que l'usuari tanqui la imatge. Si hi ha qualsevol error
        (arxiu inexistent, imatge il·legible...) mostra un missatge i
        continua l'execució.
 
        Args:
            file (str): Path de l'arxiu PNG (relatiu a ROOT_DIR o absolut).
        """
        try:
            # Si la ruta no és absoluta, la completem amb l'arrel de la
            # col·lecció
            if not os.path.isabs(file):
                full_path = os.path.join(cfg.ROOT_DIR, file)
            else:
                full_path = file
 
            # Comprovem que l'arxiu existeix abans d'obrir-lo
            if not os.path.isfile(full_path):
                print(f"ERROR: No s'ha trobat el fitxer: {full_path}")
                return
 
            # El 'with' tanca l'arxiu quan acabem; img.show() només
            # llança el visualitzador i no bloqueja
            with Image.open(full_path) as img:
                img.show()
 
        except Exception as e:
            print(f"ERROR: {e}")
 
    def show_image(self, uuid: str, mode: int = None) -> None:
        """Mostra metadades i/o imatge segons el mode (síncron).
 
        Modes:
            0: només metadades.
            1: metadades i imatge.
            2: només imatge.
 
        Quan es mostra la imatge (modes 1 i 2), espera que l'usuari premi
        ENTER abans de retornar.
 
        Args:
            uuid (str): Identificador de la imatge.
            mode (int): Mode de visualització. Si és None s'utilitza
                cfg.DISPLAY_MODE.
        """
        # Si no s'indica mode, fem servir el definit a la configuració
        if mode is None:
            mode = cfg.DISPLAY_MODE
 
        # Modes 0 i 1: imprimim les metadades
        if mode in (0, 1):
            self.print_image(uuid)
 
        # Modes 1 i 2: mostrem la imatge
        if mode in (1, 2):
            if self._image_data is None:
                print("ERROR: No es pot mostrar la imatge.")
                return
 
            # Obtenim el path de l'arxiu a partir de l'UUID
            file_path = self._image_data.get_filename(uuid)
            if file_path == "None" or file_path is None:
                print(f"ERROR: No s'ha trobat cap fitxer associat al UUID {uuid}")
                return
 
            self.show_file(file_path)
            # Pausa per fer la funció síncrona; si no hi ha entrada
            # disponible (p.ex. en un test automàtic) continuem igualment
            try:
                input("Prem ENTER per continuar...")
            except (EOFError, KeyboardInterrupt):
                pass