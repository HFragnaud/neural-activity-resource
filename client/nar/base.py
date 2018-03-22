"""

"""


class KGobject(object):
    """Base class for Knowledge Graph objects"""

    @classmethod
    def list(cls, client):
        """List all objects of this type in the Knowledge Graph"""
        return client.list(cls)

    def exists(self, client):
        """Check if this object already exists in the KnowledgeGraph"""
        # Note that this default implementation should in
        # many cases be over-ridden.
        if self.id:
            return True
        else:
            context = {"schema": "http://schema.org/"},
            query_filter = {
                "path": "schema:name",
                "op": "eq",
                "value": self.name
            }
            response = client.filter_query(self.path, query_filter, context)
            if response:
                self.id = response[0].data["@id"]
            return bool(response)

    def _save(self, data, client, exists_ok=True):
        """docstring"""
        if self.id:
            raise NotImplementedError("Update not yet implemented")
        else:
            if self.exists(client):
                if exists_ok:
                    return
                else:
                    raise ResourceExistsError(f"Already exists in the Knowledge Graph: {self!r}")
            instance = client.create_new_instance(self.__class__.path, data)
            self.id = instance.data["@id"]