"""
Copyright (C) 2024  Gigas64

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You will find a copy of this licenseIn the root directory of the project
or you can visit <https://www.gnu.org/licenses/> For further information.
"""

import os

from torch import cuda, backends
from ds_core.handlers.abstract_handlers import AbstractSourceHandler, ConnectorContract
from ds_core.handlers.abstract_handlers import HandlerFactory, AbstractPersistHandler
from sentence_transformers import SentenceTransformer
import pyarrow as pa
from nn_rag.components.commons import Commons


class ChromaSourceHandler(AbstractSourceHandler):
    """ This handler class uses the chromadb package. Chroma is the AI-native open-source
    vector database. Chroma makes it easy to build LLM apps by making knowledge, facts,
    and skills pluggable for LLMs.

        URI example
            in-memory
                uri = "chromadb:///<collection>?reference=<name>"
            to file
                uri = "chromadb:///<path>/<collection>?reference=<name>"
            to server
                uri = "chromadb://<host><port>/<collection>?reference=<name>"

        params:
            collection: The name of the collection
            reference: a prefix name to reference the document vector

        Environment:
            CHROMA_QUERY_SEARCH_LIMIT

    """

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the Connector Contract """
        # required module import
        self.chroma = HandlerFactory.get_module('chromadb')
        super().__init__(connector_contract)
        # kwargs
        _kwargs = {**self.connector_contract.kwargs, **self.connector_contract.query}
        self._reference = _kwargs.pop('reference', 'general')
        # embedding
        _embedding_name = 'all-mpnet-base-v2'
        # set device
        _device = "cuda" if cuda.is_available() else "mps" if hasattr(backends, "mps") and backends.mps.is_available() else "cpu"
        self._embedding_model = SentenceTransformer(model_name_or_path=_embedding_name, truncate_dim=384, device=_device)
        # search
        self._search_limit = int(os.environ.get('CHROMA_QUERY_SEARCH_LIMIT', _kwargs.pop('search_limit', '10')))
        # server
        _path, _, _collection_name = self.connector_contract.path.rpartition('/')
        self._collection_name = _collection_name if (isinstance(_collection_name, str) and
                                                     len(_collection_name) >= 3) else 'default'
        if self.connector_contract.hostname and self.connector_contract.port:
            self._client = self.chroma.HttpClient(host=self.connector_contract.hostname,
                                                  port=self.connector_contract.port)
        elif _path:
            self._client = self.chroma.PersistentClient(path=_path[1:])
        else:
            self._client = self.chroma.Client()
        self._collection = self._client.get_or_create_collection(name=self._collection_name)

    def supported_types(self) -> list:
        """ The source types supported with this module"""
        return ['chromadb']

    def exists(self) -> bool:
        """If the table exists"""
        return True

    def has_changed(self) -> bool:
        return True

    def reset_changed(self, changed: bool = False):
        pass

    def load_canonical(self, query: [str, list], expr: dict=None, limit: int=None, **kwargs) -> pa.Table:
        """ returns the canonical dataset based on a vector similarity search
            see: https://cookbook.chromadb.dev/core/filters/
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The Connector Contract is not valid")
        query = Commons.list_formatter(query)
        expr = expr if isinstance(expr, dict) else None
        limit = limit if isinstance(limit, int) else self._search_limit
        # query
        if expr:
            results = self._collection.query(
                query_texts=query,
                n_results=limit,
                where=expr
            )
        else:
            results = self._collection.query(query_texts=query, n_results=limit)
        # build table
        ids = pa.array(results.get('ids')[0], pa.string())
        distances = pa.array(results.get('distances')[0], pa.float32())
        entities = pa.array(results.get('documents')[0], pa.string())
        return pa.table([ids, distances, entities], names=['id', 'distance', 'text'])

class ChromaPersistHandler(ChromaSourceHandler, AbstractPersistHandler):
    # a Chroma persist handler

    def persist_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ persists the canonical dataset"""
        return self.backup_canonical(canonical=canonical, **kwargs)

    def backup_canonical(self, canonical: pa.Table, **kwargs) -> bool:
        """ creates a backup of the canonical to an alternative table  """
        if not isinstance(self.connector_contract, ConnectorContract):
            return False
        _params = kwargs
        chunks = canonical.to_pylist()
        text_chunks = [item["text"] for item in chunks]
        embeddings = self._embedding_model.encode(text_chunks)

        self._collection.upsert(
            ids=[f"{str(self._reference)}_{str(i)}" for i in range(len(text_chunks))],
            metadatas=[{'reference': self._reference}] * len(text_chunks),
            documents=text_chunks,
            embeddings=embeddings,
        )
        return

    def remove_canonical(self) -> bool:
        """removes the collection"""
        self._collection.delete(
            where={"metadata": self._reference}
        )
        return True

    def remove_collection(self) -> bool:
        """remove a collection"""
        self._client.delete_collection(self._collection_name)
        return True
