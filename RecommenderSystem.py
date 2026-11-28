"""
RecommenderSystem.py - Student Template for Image Recommendation System

This class implements the recommendation system for Phase 2 and Phase 3 of the project.
It uses CLIP embeddings to find similar images and generate transition paths.

IMPORTANT NOTES FOR STUDENTS:
- Fill in the methods below with your own implementation
- Keep the method signatures exactly as shown (parameters and return types)
- You can add helper methods if needed
- The cosine_similarity function is provided for your convenience


Phases:
- Phase 2: find_similar_images() - Find k most similar images
- Phase 3: find_transition_prompts() - Find path connecting two images
"""

import json
from datetime import datetime
import math
import os
from Submission_1.Gallery import Gallery
import heapq
import re


class RecommenderSystem:
    """
    Recommender system for finding similar images and generating transition paths.

    Attributes:
        
        vectors_path: Path to the JSON file containing CLIP vectors
    """

    def __init__(self, vectors_path: str, image_data=None, image_id=None):
        """
        Initialize the recommender system by loading CLIP vectors.

        Args:
            vectors_path: Path to JSON file with CLIP embeddings
                         Format: {"uuid": {"image_embedding": [...], "text_embedding": [...]}, ...}
            image_data: (Optional) ImageData instance from Phase 1 for metadata access
            image_id: (Optional) ImageID instance from Phase 1 for UUID mapping
        """
        self.vectors_path = vectors_path
        self.image_data = image_data
        self.image_id = image_id
        # TODO: Load vectors from JSON file
        # Structure should be: self.vectors = {uuid: {image_embedding: [...], text_embedding: [...]}}
        self.vectors = {}
        self.uuid_de_clau = {}
        self.clau_de_uuid = {}
        self.claus = []
        self.image_matrix = []
        self.pos = {}
        self.norm_image = {}
        self.norm_text = {}
        self._preparat = False

        try:
            with open(vectors_path, "r", encoding = "utf-8") as f:
                dades = json.load(f)
            if isinstance(dades, dict):
                brut = dades.get("vectors", dades)
                self.vectors = {clau: entrada for clau, entrada in brut.items()
                                if isinstance(entrada, dict)}

        except FileNotFoundError:
            print(f"ERROR: No s'ha trobat el fitxer de vectors: {vectors_path}")
        except (json.JSONDecodeError, OSError) as e:
            print(f"ERROR llegint {vectors_path}: {e}")

        self._construir_mapes()

    def _construir_mapes(self) -> None:
        self.uuid_de_clau = {}
        self.clau_de_uuid = {}

        per_nom = {}
        if self.image_data is not None:
            for uuid in self.image_data:
                fitxer = self.image_data.get_filename(uuid)
                if fitxer:
                    nom = os.path.splitext(os.path.basename(fitxer))[0]
                    per_nom[nom] = uuid

        if self.image_id is None and not per_nom:
            return

        for clau in self.vectors:
            uuid = None
            if self.image_id is not None:
                uuid = self.image_id.get_uuid(clau + ".png")
            if uuid is None:
                uuid = per_nom.get(clau)
            if uuid is not None:
                self.uuid_de_clau[clau] = uuid
                self.clau_de_uuid[uuid] = clau

    def _clau (self, identificador): 
        if identificador in self.vectors:
            return identificador
        return self.clau_de_uuid.get(identificador)

    @staticmethod
    def _normalitzar(vec) -> list:
        norma = math.sqrt(sum(x * x for x in vec))
        if norma == 0:
            return list(vec)
        return [x / norma for x in vec]


    def preprocess(self):
        """
        Preprocess and prepare data structures for efficient queries.

        This method is called once before running Phase 2/3 queries.
        Use it to build indexes or prepare other data structures
        that will speed up similarity computations.

        """
        # TODO: Implement preprocessing
        self.claus = []
        self.image_matrix = []
        self.pos = {}
        self.norm_image = {}
        self.norm_text = {}

        self._construir_mapes()

        for clau, entrada in self.vectors.items():
            emb_imatge = entrada.get("image_embedding")
            if emb_imatge:
                entrada["image_embedding"] = self._normalitzar(emb_imatge)
                normalitzat = entrada["image_embedding"]
                self.pos[clau] = len(self.claus)
                self.claus.append(clau)
                self.image_matrix.append(normalitzat)
                self.norm_image[clau] = normalitzat

            emb_text = entrada.get("text_embedding")
            if emb_text:
                entrada["text_embedding"] = self._normalitzar(emb_text)
                self.norm_text[clau] = entrada["text_embedding"]

        self._preparat = True

    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        """
        Compute cosine similarity between two vectors.

        Cosine similarity measures the angle between vectors:
        - 1.0 = identical direction (very similar)
        - 0.0 = perpendicular (not related)
        - -1.0 = opposite direction (very different)

        Args:
            vec_a: First vector (list of floats)
            vec_b: Second vector (list of floats)

        Returns:
            float: Cosine similarity score between -1.0 and 1.0

        Formula:
            similarity = (a · b) / (||a|| * ||b||)
            where · is dot product and ||a|| is the magnitude (norm) of vector a

        Implementation tips:
        - Handle edge cases: empty vectors, zero norms
        
        # Calculate dot product
        dot = sum(a * b for a, b in zip(vec_a, vec_b))

        # Calculate magnitudes (norms)
        norm_a = sum(a * a for a in vec_a) ** 0.5
        norm_b = sum(b * b for b in vec_b) ** 0.5

        # Return similarity (handle division by zero)
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0
        """
        return sum(a * b for a, b in zip(vec_a, vec_b)) #Com ja tenim calculats els vectors normalitzats no cal tornar-ho a fer

    def find_similar_images(self, query_uuid: str, k: int = 10) -> Gallery:
        """
        Find k most similar images to a query image.

        PHASE 2: This is the main evaluation method for Phase 2.

        Args:
            query_uuid: UUID of the query image
            k: Number of similar images to return (default 10)

        Returns:
            Gallery object with images field containing top-k similar UUIDs
            ordered from most to least similar

        Example:
            system = RecommenderSystem("vectors.json")
            system.preprocess()
            gallery = system.find_similar_images("uuid_123", k=10)
            print(gallery.images)  # ['uuid_45', 'uuid_67', ..., 'uuid_99']

        Evaluation:
        - Metric: Recall@100 (your top-10 vs ground truth top-100)
        - Timing: Tested on 1,000 queries
        - Scoring: 25 pts for precision + 15 pts for speed


        TODO: Implement this method
        """
        # TODO:
        # 1. Get query vector from self.vectors
        # 2. Calculate similarity to other images (use cosine_similarity)
        # 3. Sort by similarity (descending)
        # 4. Create and return Gallery with top-k images

        gallery = Gallery()
        gallery.images = []
        if not self._preparat:
            self.preprocess()

        clau_consulta = self._clau(query_uuid)
        vector_consulta = self.norm_image.get(clau_consulta)

        if vector_consulta is None or k <= 0:
            return gallery

        similituts = []

        for clau, vector in self.norm_image.items():
            if clau == clau_consulta:  # S'exclou la imatge de la query
                continue

            similitud = self.cosine_similarity(vector_consulta, vector)
            similituts.append((similitud, clau))

        top = heapq.nlargest(k, similituts, key=lambda imatge: imatge[0])

        for similitud, clau in top:
            uuid = self.uuid_de_clau.get(clau, clau)
            gallery.images.append(uuid)
        return gallery

    def find_transition_prompts(self, uuid_1: str, uuid_2: str) -> list:
        """
        Find a transition path of prompts connecting two images.

        PHASE 3: This is the main evaluation method for Phase 3.

        Args:
            uuid_1: Starting image UUID
            uuid_2: Destination image UUID

        Returns:
            List of prompts describing the visual transition from uuid_1 to uuid_2
            First element should be prompt of uuid_1, last should be prompt of uuid_2
            Length of list represents number of transition steps

        Example:
            prompts = system.find_transition_prompts(uuid_start, uuid_end)
            # Returns: [
            #   "a cat in the snow",          # uuid_start
            #   "an animal in the snow",      # intermediate
            #   "a creature in the snow",     # intermediate
            #   "a dragon in the snow",       # intermediate
            #   "a dragon by a mountain",     # uuid_end
            # ]

        Evaluation:
        - Metric: Word overlap (how many words match ground truth)
        - Timing: Tested on ~10 transitions
        - Scoring: 30 pts for quality + 10 pts for speed

        Algorithm overview:
        1. Get prompts for both images (use image_data if available)
        2. Extract meaningful words from prompts (stop word removal)
        3. Build a graph where nodes are images and edges connect similar images
        4. Return prompts along a path

        Key considerations:
        - Path quality: Should gradually transition from uuid_1 to uuid_2
        - Path length: Shorter paths are faster but may skip important intermediates

        TODO: Implement this method
        """
       
        # TODO:
        # 1. Validate that both UUIDs exist
        # 2. Get prompts using self.image_data if available
        # 3. Build set of images to explore
        # 4. Build similarity graph between candidates
        # 5. Find path
        # 6. Extract and return prompts from path

        self._ultim_cami = []
        if not self._preparat:
            self.preprocess()

        inici = self._clau(uuid_1)
        final = self._clau(uuid_2)

        if inici not in self.norm_image or final not in self.norm_image:
            return []

        if self.image_data is None:
            return []

        prompts = {}

        for clau in [inici, final]:
            uuid = self.uuid_de_clau.get(clau, clau)
            prompt = self.image_data.get_prompt(uuid)

            if not prompt or prompt == "None":
                return []

            prompts[clau] = prompt

        if inici == final:
            return [prompts[inici]]

        candidats = {inici, final}

        similituds_inici = []
        similituds_final = []
        similituds_pont = []

        for clau, vector in self.norm_image.items():

            if clau == inici or clau == final:
                continue

            uuid = self.uuid_de_clau.get(clau, clau)
            prompt = self.image_data.get_prompt(uuid)

            if not prompt or prompt == "None":
                continue

            sim_inici = self.cosine_similarity(
                self.norm_image[inici],
                vector
            )

            sim_final = self.cosine_similarity(
                self.norm_image[final],
                vector
            )

            sim_pont = min(sim_inici, sim_final)

            similituds_inici.append((sim_inici, clau))
            similituds_final.append((sim_final, clau))
            similituds_pont.append((sim_pont, clau))

        for similituds in [
            similituds_inici,
            similituds_final,
            similituds_pont
        ]:

            top = heapq.nlargest(50, similituds)

            for similitud, clau in top:
                candidats.add(clau)

        for clau in sorted(candidats):

            uuid = self.uuid_de_clau.get(clau, clau)
            prompt = self.image_data.get_prompt(uuid)

            if prompt and prompt != "None":
                prompts[clau] = prompt

        
       
        #Graf
        graf = {clau: {} for clau in prompts}
        nodes = list(graf)

        for i in range(len(nodes)):

            a = nodes[i]

            for j in range(i + 1, len(nodes)):

                b = nodes[j]

                similitud = self.cosine_similarity(
                    self.norm_image[a],
                    self.norm_image[b]
                )

                pes = (1 - similitud) ** 2

                graf[a][b] = pes
                graf[b][a] = pes




        #Dijsktra
        distancies = {inici: 0}
        predecessors = {}
        cua = [(0, inici)]

        while cua:
            distancia, actual = heapq.heappop(cua)

            if distancia > distancies[actual]:
                continue

            if actual == final:
                break

            for vei, pes in graf[actual].items():
                nova_distancia = distancia + pes

                if nova_distancia < distancies.get(vei, math.inf):
                    distancies[vei] = nova_distancia
                    predecessors[vei] = actual
                    heapq.heappush(cua, (nova_distancia, vei))

        if final not in distancies:
            return []

        cami = [final]

        while cami[-1] != inici:
            cami.append(predecessors[cami[-1]])

        cami.reverse()

        self._ultim_cami = cami

        return [prompts[clau] for clau in cami]
