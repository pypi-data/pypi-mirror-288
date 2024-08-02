from pyalbert.config import ELASTICSEARCH_IX_VER, QDRANT_IX_VER


def create_index(index_name, index_type, add_doc=True, recreate=False, storage_dir=None, batch_size=None):
    if index_type == "bm25":
        from .elasticsearch import create_bm25_index

        print(f"Creating Elasticsearch index for '{index_name}-{ELASTICSEARCH_IX_VER}' ...")
        return create_bm25_index(index_name, add_doc, recreate, storage_dir=storage_dir)
    elif index_type == "e5":
        from .qdrant import create_vector_index

        print(f"Creating Qdrant index for '{index_name}-{QDRANT_IX_VER}' ...")
        return create_vector_index(index_name, add_doc, recreate, storage_dir=storage_dir, batch_size=batch_size)
    else:
        raise NotImplementedError("index type unknown: %s" % index_type)
