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
from ds_core.handlers.abstract_handlers import AbstractSourceHandler, ConnectorContract
from ds_core.handlers.abstract_handlers import HandlerFactory, AbstractPersistHandler
from sentence_transformers import SentenceTransformer
from torch import cuda, backends
import pyarrow as pa

__author__ = 'Darryl Oatridge'


class MilvusSourceHandler(AbstractSourceHandler):
    """ This handler class uses pymilvus package. Milvus is an open-source vector
    database designed to manage and search large-scale vector data. It is designed to
    store, index, and search vector data efficiently, targeting AI-driven applications
    that require efficient handling of unstructured data.

        URI example
            uri = "milvus://host:port/database?collection=<name>&reference=<name>"

        params:
            collection: The name of the collection
            reference: a prefix name to reference the document vector

        Environment:
            MILVUS_INDEX_CLUSTERS
            MILVUS_QUERY_NUM_SIMILARITY
            MILVUS_QUERY_SEARCH_LIMIT
    """

    def __init__(self, connector_contract: ConnectorContract):
        """ initialise the Handler passing the Connector Contract """
        # required module import
        self.pymilvus = HandlerFactory.get_module('pymilvus')
        super().__init__(connector_contract)
        # reset to use dialect
        _kwargs = {**self.connector_contract.kwargs, **self.connector_contract.query}
        _database = self.connector_contract.path[1:] if self.connector_contract.path[1:] else 'rai'
        self._reference = _kwargs.pop('reference', 'general')
        self._collection_name = _kwargs.pop('collection', "default")
        self._index_clusters = int(os.environ.get('MILVUS_INDEX_CLUSTERS', _kwargs.pop('index_clusters', '128')))
        self._search_limit = int(os.environ.get('MILVUS_QUERY_SEARCH_LIMIT', _kwargs.pop('search_limit', '8')))
        self._query_similarity = int(os.environ.get('MILVUS_QUERY_NUM_SIMILARITY', _kwargs.pop('query_similarity', '10')))
        # embedding
        _embedding_name = 'all-mpnet-base-v2'
        # device
        _device = "cuda" if cuda.is_available() else "mps" if hasattr(backends, "mps") and backends.mps.is_available() else "cpu"
        # embedding model
        self._embedding_model = SentenceTransformer(model_name_or_path=_embedding_name, device=_device)
        _dimensions = self._embedding_model.get_sentence_embedding_dimension()
        # Environment hyperparams
        self._index_clusters = int(os.environ.get('MILVUS_INDEX_CLUSTERS', _kwargs.pop('index_clusters', '128')))
        self._search_limit = int(os.environ.get('MILVUS_QUERY_SEARCH_LIMIT', _kwargs.pop('search_limit', '10')))
        self._query_similarity = int(os.environ.get('MILVUS_QUERY_NUM_SIMILARITY', _kwargs.pop('query_similarity', '10')))
        # Start the server
        self.pymilvus.connections.connect(host=connector_contract.hostname, port=connector_contract.port)
        if _database in self.pymilvus.db.list_database():
            self.pymilvus.db.using_database(_database)
        else:
            self.pymilvus.db.create_database(_database)
        # Create the collection
        if self.pymilvus.utility.has_collection(self._collection_name):
            self._collection = self.pymilvus.Collection(self._collection_name)
        else:
            fields = [
                self.pymilvus.FieldSchema(name="id", dtype=self.pymilvus.DataType.VARCHAR, auto_id=False, is_primary=True, max_length=64),
                self.pymilvus.FieldSchema(name="source", dtype=self.pymilvus.DataType.VARCHAR, max_length=2048),
                self.pymilvus.FieldSchema(name="embeddings", dtype=self.pymilvus.DataType.FLOAT_VECTOR, dim=_dimensions)
            ]
            # schema
            schema = self.pymilvus.CollectionSchema(fields=fields)
            # collection
            self._collection = self.pymilvus.Collection(
                name=self._collection_name,
                schema=schema,
                num_shards=2,
                consistency_level='Strong')
            # index
            index_params = {
                "metric_type": 'COSINE',
                "index_type": "IVF_FLAT",
                "params": {"nlist": self._index_clusters}
            }
            self._collection.create_index("embeddings", index_params)
        self._changed_flag = True

    def supported_types(self) -> list:
        """ The source types supported with this module"""
        return ['milvus']

    def exists(self) -> bool:
        """If the table exists"""
        return True

    def has_changed(self) -> bool:
        """ if the table has changed. Only works with certain implementations"""
        return self._changed_flag

    def reset_changed(self, changed: bool = False):
        """ manual reset to say the table has been seen. This is automatically called if the file is loaded"""
        changed = changed if isinstance(changed, bool) else False
        self._changed_flag = changed

    def load_canonical(self, query: [str, list], expr: str=None, limit: int=None, **kwargs) -> pa.Table:
        """ returns the canonical dataset based on a vector similarity search

            search(
                data: list[list[float]],
                anns_field: str,
                param: dict,
                limit: int
                expr: str | None,
                output_fields: list[str] | None,
                timeout: float | None,
                round_decimal: int
                )
)
        """
        if not isinstance(self.connector_contract, ConnectorContract):
            raise ValueError("The Connector Contract is not valid")
        expr = expr if isinstance(expr, str) else None
        limit = limit if isinstance(limit, int) else self._search_limit
        # get collection
        if not self._collection:
            self._collection = self.pymilvus.Collection(self._collection_name)
        self._collection.load()
        # embedding
        query_vector = self._embedding_model.encode(query)
        # search
        params = {"metric_type": "COSINE", "params": {"nprobe": self._query_similarity}}
        results = self._collection.search(
            data = [query_vector],
            anns_field = "embeddings",
            param = params,
            expr = expr,
            limit = limit,
            output_fields=["source"])
        self._collection.release()
        # build table
        ids = pa.array(results[0].ids, pa.string())
        distances = pa.array(results[0].distances, pa.float32())
        entities = pa.array([x.entity.to_dict()['entity']['source'] for x in results[0]], pa.string())
        return pa.table([ids, distances, entities], names=['id', 'distance', 'text'])


class MilvusPersistHandler(MilvusSourceHandler, AbstractPersistHandler):
    # a Milvus persist handler

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
        data = [
            [f"{str(self._reference)}_{str(i)}" for i in range(len(text_chunks))],
            text_chunks,
            embeddings
        ]
        if not self._collection:
            self._collection = self.pymilvus.Collection(self._collection_name)
        self._collection.load()
        self._collection.upsert(data=data)
        self._collection.release()
        return

    def remove_canonical(self) -> bool:
        """removes a document reference"""
        if self.pymilvus.utility.has_collection(self._collection_name):
            if not self._collection:
                self._collection = self.pymilvus.Collection(self._collection_name)
            expr = f"id like \"{str(self._reference)}_\""
            self._collection.load()
            self._collection.delete(expr)
            self._collection.release()
        return True

    def remove_collection(self) -> bool:
        """remove a collection"""
        if self.pymilvus.utility.has_collection(self._collection_name):
            self.pymilvus.utility.drop_collection(self._collection_name)
        return True
