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
 
class ImageData():
    """Emmagatzema en memòria les metadades de les imatges de la col·lecció.
 
    Estructura de dades interna:
        self._imatges (dict): diccionari que té com a clau l'UUID de la
        imatge (str) i com a valor un altre diccionari amb dues claus:
 
            {
                'file': str,       # path relatiu de l'arxiu PNG
                'metadata': dict   # camps de metadades (buit fins que es
                                   # crida a load_metadata)
            }
 
        El diccionari 'metadata' conté els camps prompt, model, seed,
        cfg_scale, steps, sampler, generated i created_date (tots str) i
        la clau 'dimensions', que guarda una tupla (width, height).
 
    S'ha escollit un diccionari (taula de hash) perquè permet inserir,
    consultar i esborrar una imatge a partir del seu UUID en temps mitjà
    O(1), sense haver de recórrer cap llista.
    """
 
    # Llista dels camps de metadades obligatoris (només informativa; els
    # mètodes de la classe no la fan servir actualment).
    CAMPS = ['prompt', 'seed', 'cfg_scale', 'steps',
             'sampler', 'model', 'generated', 'created_date']
 
    def __init__(self):
        """Crea la col·lecció buida (cap imatge registrada)."""
        self._imatges = {}
 
    def __len__(self) -> int:
        """Retorna el nombre d'imatges registrades."""
        return len(self._imatges)
 
    def __str__(self) -> str:
        """Retorna una descripció textual amb el nombre d'imatges."""
        return f"ImageData: {len(self._imatges)} imatges registrades"
 
    def __iter__(self):
        """Permet recórrer els UUID de les imatges registrades."""
        return iter(self._imatges)
 
    def __contains__(self, uuid) -> bool:
        """Indica si l'UUID donat està registrat (operador 'in')."""
        if uuid is None:
            return False
        return str(uuid) in self._imatges
 
    def __getitem__(self, uuid):
        """Retorna l'entrada completa de la imatge (o None si no existeix)."""
        if uuid is None:
            return None
        return self._imatges.get(str(uuid))
 
    def add_image(self, uuid: str, file: str) -> None:
        """Crea l'entrada d'una imatge amb el seu UUID i el path de l'arxiu.
 
        Les metadades queden buides fins que es cridi a load_metadata().
        Si l'UUID ja existeix, l'entrada no se sobreescriu.
 
        Args:
            uuid (str): Identificador únic de la imatge.
            file (str): Path relatiu de l'arxiu PNG.
        """
        # Ignorem paràmetres nuls, que no siguin str o que estiguin buits
        if uuid is None or file is None:
            return
        if not isinstance(uuid, str) or not isinstance(file, str):
            return
        if not uuid or not file:
            return
 
        # Només creem l'entrada si l'UUID encara no està registrat
        uuid_str = str(uuid)
        if uuid_str not in self._imatges:
            self._imatges[uuid_str] = {
                'file': file,
                'metadata': {}
            }
 
    def remove_image(self, uuid: str) -> None:
        """Elimina la imatge i les seves metadades (si existeix)."""
        if uuid is None:
            return
        uuid_str = str(uuid)
        # pop() amb valor per defecte no falla si l'UUID no existeix
        self._imatges.pop(uuid_str, None)
 
    def get_filename(self, uuid: str) -> str:
        """Retorna el path relatiu de l'arxiu associat a l'UUID.
 
        Returns:
            str: El path guardat a add_image(), o None si l'UUID no existeix.
        """
        if uuid is None:
            return None
        uuid_str = str(uuid)
        entrada = self._imatges.get(uuid_str)
        return entrada['file'] if entrada else None
 
    def get_file(self, uuid: str) -> str:
        """Àlies de get_filename()."""
        return self.get_filename(uuid)
 
    @staticmethod
    def _find_file(file: str) -> str:
        """Resol el path complet d'un arxiu de la col·lecció.
 
        Prova diverses ubicacions possibles (relatives a l'arrel de la
        col·lecció, al directori actual, etc.) i retorna la primera que
        existeix al disc.
 
        Args:
            file (str): Path (relatiu o absolut) de l'arxiu.
 
        Returns:
            str: Path complet de l'arxiu. Si no es troba enlloc, retorna
            el path relatiu unit a l'arrel de la col·lecció.
        """
        if not file or not isinstance(file, str):
            return None
        # Si el path ja és absolut, el fem servir tal qual
        if os.path.isabs(file):
            return file
        # Possibles ubicacions de l'arxiu, per ordre de preferència
        candidates = [
            os.path.join(cfg.get_root(), file),
            os.path.join(cfg.ROOT_DIR, file),
            file,
        ]
        # Si el path inclou el prefix 'generated_images/', també provem
        # sense aquest prefix
        norm = file.replace("\\", "/")
        if "generated_images/" in norm:
            sub = norm.split("generated_images/")[-1]
            candidates.extend([
                os.path.join(cfg.get_root(), sub),
                os.path.join(cfg.ROOT_DIR, sub),
                sub,
            ])
        # Retornem el primer candidat que existeixi realment al disc
        for c in candidates:
            if os.path.isfile(c):
                return c
        return os.path.join(cfg.get_root(), file)
 
    def load_metadata(self, uuid: str) -> None:
        """Llegeix les metadades embegudes en el PNG i les guarda en memòria.
 
        Es pot cridar diverses vegades: cada crida substitueix les
        metadades anteriors per les que hi ha ara a l'arxiu.
 
        Args:
            uuid (str): UUID de la imatge (també s'accepta el path de
                l'arxiu, que es cerca entre les entrades registrades).
 
        Raises:
            FileNotFoundError: Si l'UUID no està registrat o l'arxiu no
                existeix al disc.
        """
        # Si no es passa cap identificador, no hi ha res a fer
        if not uuid:
            return
 
        uuid_str = str(uuid)
        # Si l'UUID no està registrat, provem d'interpretar el paràmetre
        # com el path de l'arxiu i cerquem l'entrada que el té guardat
        if uuid_str not in self._imatges:
            target_uuid = None
            for u, d in self._imatges.items():
                if d.get('file') == uuid or d.get('file') == uuid_str:
                    target_uuid = u
                    break
            if target_uuid is not None:
                uuid_str = target_uuid
            else:
                # Ni com a UUID ni com a path: la imatge no existeix
                raise FileNotFoundError(f"UUID desconegut: {uuid}")
 
        entrada = self._imatges[uuid_str]
        full_path = self._find_file(entrada['file'])
 
        try:
            with Image.open(full_path) as img:
                # Llegim els text chunks del PNG; si la funció de cfg no
                # retorna res, recorrem a img.text de Pillow
                raw_text = cfg.read_png_metadata(full_path)
                if raw_text is None:
                    raw_text = getattr(img, "text", {}) or {}
                # Passem les claus a minúscules i els valors a str, de
                # manera que 'CFG_Scale' passa a ser 'cfg_scale'
                text_meta = {str(k).lower(): str(v) for k, v in raw_text.items()}
 
                # Alguns camps admeten un nom alternatiu
                cfg_val = text_meta.get('cfg_scale', text_meta.get('cfg', 'None'))
                date_val = text_meta.get('created_date', text_meta.get('date', 'None'))
 
                # Substituïm les metadades; un camp absent es guarda com
                # a 'None' (string), tal com demana l'enunciat
                entrada['metadata'] = {
                    'prompt': text_meta.get('prompt', 'None'),
                    'model': text_meta.get('model', 'None'),
                    'seed': text_meta.get('seed', 'None'),
                    'cfg_scale': cfg_val,
                    'steps': text_meta.get('steps', 'None'),
                    'sampler': text_meta.get('sampler', 'None'),
                    'generated': text_meta.get('generated', 'None'),
                    'created_date': date_val,
                    'dimensions': (img.width, img.height)
                }
        except FileNotFoundError:
            # Si l'arxiu no existeix, deixem que l'error pugi
            raise
        except Exception:
            # Qualsevol altre error de lectura: deixem les metadades buides
            entrada['metadata'] = {}
 
    def _get_field(self, uuid: str, field: str) -> str:
        """Retorna el valor d'un camp de metadades com a string.
 
        Mètode auxiliar que fan servir tots els get_*() de metadades.
 
        Returns:
            str: El valor del camp, o None si l'UUID no existeix o les
            metadades encara no s'han carregat.
        """
        if uuid is None:
            return None
        uuid_str = str(uuid)
        entrada = self._imatges.get(uuid_str)
        if entrada is None:
            return None
        meta = entrada.get('metadata', {})
        if field not in meta:
            return None
        return str(meta[field])
 
    def get_prompt(self, uuid: str) -> str:
        """Retorna el prompt utilitzat per generar la imatge."""
        return self._get_field(uuid, 'prompt')
 
    def get_model(self, uuid: str) -> str:
        """Retorna el model d'IA utilitzat."""
        return self._get_field(uuid, 'model')
 
    def get_seed(self, uuid: str) -> str:
        """Retorna la llavor aleatòria (seed) utilitzada."""
        return self._get_field(uuid, 'seed')
 
    def get_cfg_scale(self, uuid: str) -> str:
        """Retorna el CFG Scale (guidance scale) utilitzat."""
        return self._get_field(uuid, 'cfg_scale')
 
    def get_steps(self, uuid: str) -> str:
        """Retorna el nombre de passos d'iteració del model."""
        return self._get_field(uuid, 'steps')
 
    def get_sampler(self, uuid: str) -> str:
        """Retorna l'algorisme de mostreig utilitzat."""
        return self._get_field(uuid, 'sampler')
 
    def get_generated(self, uuid: str) -> str:
        """Retorna el camp 'generated' (normalment 'true')."""
        return self._get_field(uuid, 'generated')
 
    def get_created_date(self, uuid: str) -> str:
        """Retorna la data de creació (format YYYY-MM-DD)."""
        return self._get_field(uuid, 'created_date')
 
    def get_dimensions(self, uuid: str) -> tuple:
        """Retorna la tupla (width, height) de la imatge.
 
        Returns:
            tuple: Les dimensions llegides a load_metadata(), o None si
            l'UUID no existeix o les metadades encara no s'han carregat.
        """
        if uuid is None:
            return None
        uuid_str = str(uuid)
        entrada = self._imatges.get(uuid_str)
        if entrada is None:
            return None
        # Les dimensions es guarden dins del diccionari 'metadata'
        return entrada.get('metadata', {}).get('dimensions', None)