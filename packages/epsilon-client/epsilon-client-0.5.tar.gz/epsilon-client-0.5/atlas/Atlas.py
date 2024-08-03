import requests


class AtlasClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)
        self.headers = {
            'Content-Type': 'application/json;charset=utf-8',
        }

    def create_entity(self, entity):
        url = f"{self.base_url}/api/atlas/v2/entity"
        payload = {"entity": entity.entity}
        response = requests.post(url, headers=self.headers, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def create_bulk_entities(self, entities):
        url = f"{self.base_url}/api/atlas/v2/entity/bulk"
        payload = {"entities": [entity.entity for entity in entities]}
        response = requests.post(url, headers=self.headers, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()


class AtlasEntity:
    def __init__(self, type_name, attributes, status="ACTIVE"):
        self.entity = {
            "typeName": type_name,
            "status": status,
            "attributes": attributes
        }


class AtlasColumn(AtlasEntity):
    def __init__(self, name, owner, table_guid, data_type, description):
        attributes = {
            "owner": owner,
            "ownerName": owner,
            "name": name,
            "qualifiedName": name,
            "default_value": None,
            "isPrimaryKey": False,
            "indexes": [],
            "isNullable": False,
            "data_type": data_type,
            "description": description,
            "table": {
                "guid": table_guid,
                "typeName": "rdbms_table"
            }
        }
        super().__init__("rdbms_column", attributes)


class AtlasDatabase(AtlasEntity):
    def __init__(self, name, owner, instance_guid):
        attributes = {
            "displayName": name,
            "name": name,
            "owner": owner,
            "qualifiedName": name,
            "userDescription": None
        }
        relationship_attributes = {
            "instance": {
                "guid": instance_guid,
                "typeName": "rdbms_instance"
            }
        }
        super().__init__("rdbms_db", attributes)
        self.entity["relationshipAttributes"] = relationship_attributes

    @staticmethod
    def extract_guid(response):
        # Extract the GUID from the response
        return list(response['guidAssignments'].values())[0]


class AtlasDatasource(AtlasEntity):
    def __init__(self, name, owner, hostname, port, description, contact_info):
        attributes = {
            "owner": owner,
            "ownerName": owner,
            "name": name,
            "qualifiedName": name,
            "rdbms_type": "postgres",
            "description": description,
            "contact_info": contact_info,
            "platform": "Linux",
            "hostname": hostname,
            "protocol": "postgres protocol",
            "port": port
        }
        super().__init__("rdbms_instance", attributes)

    @staticmethod
    def extract_guid(response):
        # Extract the GUID from the response
        return list(response['guidAssignments'].values())[0]

class AtlasTable(AtlasEntity):

    def __init__(self, name, owner, db_guid):
        attributes = {
            "owner": owner,
            "ownerName": owner,
            "name": name,
            "db": {
                "guid": db_guid,
                "typeName": "rdbms_db"
            },
            "qualifiedName": name,
            "description": "table description details"
        }
        super().__init__("rdbms_table", attributes)

    @staticmethod
    def extract_guid(response):
        # Extract the GUID from the response
        return list(response['guidAssignments'].values())[0]
