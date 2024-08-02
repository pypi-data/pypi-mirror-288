from typing import List, Optional
from matplotlib.figure import Figure
import umap
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)


class EmbeddingsVisualisor:
    def __init__(self, all_embeddings) -> None:
        logger.info('init is called')

        self.all_embeddings = all_embeddings
        self._all_embeddings_2d = None
        self.umap_transform = self.get_umap_transform()

    def get_umap_transform(self, random_state=0, transform_seed=0):
        umap_transform = umap.UMAP(
            random_state=random_state, transform_seed=transform_seed).fit(self.all_embeddings)
        return umap_transform

    def convert_embeddings_to_2D(self, embeddings):
        umap_embeddings = np.empty((len(embeddings), 2))
        for i, embedding in enumerate(tqdm(embeddings)):
            umap_embeddings[i] = self.umap_transform.transform([embedding])
        return umap_embeddings

    def visualise(self, 
                  title: str, 
                  query_embeddings: List[float], 
                  document_embeddings: List[List[float]], 
                  figure: Optional[Figure] = None) -> Figure:
        """
        - Makes similariy search and retrieves documents
        - Displays
            - Creates gray dots for 'documents'
            - Marks 'query embedding' with 'red X'
            - Marks 'retrieved documents embeddings' with 'green circle'

        ### Example

        if you want to add more scatter.

        Every visualise calls `plt.figure()` means 
        'Create a new figure, or activate an existing figure.'

        ```
        figure = visualise(...)
        plt.figure(num=figure)
        plt.scatter(data_2d[:, 0], data_2d[:, 1], 
                    s=150, marker='X', color='r')
        ```
        """
        logger.info('starting visualisation.')

        if self._all_embeddings_2d is None:
            logger.info('converting all document embeddings to 2D.')
            self._all_embeddings_2d = self.convert_embeddings_to_2D(
                self.all_embeddings)

        logger.info('converting query embeddings to 2D')
        query_embeddings_2d = self.convert_embeddings_to_2D([query_embeddings])

        logger.info('converting retrieved document embeddings to 2D.')
        document_embeddings_2d = self.convert_embeddings_to_2D(
            document_embeddings)

        # Plot the projected query and retrieved documents in the embedding space
        logger.info('visualise pyplot.')
        figure = plt.figure(num=figure)
        plt.scatter(
            self._all_embeddings_2d[:, 0], self._all_embeddings_2d[:, 1], s=10, color='gray')
        plt.scatter(
            query_embeddings_2d[:, 0], query_embeddings_2d[:, 1], s=150, marker='X', color='r')
        plt.scatter(
            document_embeddings_2d[:, 0], document_embeddings_2d[:, 1], s=100, facecolors='none', edgecolors='g')

        plt.gca().set_aspect('equal', 'datalim')
        plt.title(f'{title}')
        plt.axis('off')

        return figure
