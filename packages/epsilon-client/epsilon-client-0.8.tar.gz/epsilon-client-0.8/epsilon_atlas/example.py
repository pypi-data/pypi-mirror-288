from Atlas import AtlasClient, AtlasDatasource, AtlasDatabase, AtlasTable, AtlasColumn
from Reader import DataReader

base_url = ""
username = ""
password = ""
file_path = ""
project_name = ""
contact_email = ""


def main():
    data_reader = DataReader(file_path)
    columns, data, types = data_reader.read_data()
    atlas_client = AtlasClient(base_url, username, password)

    # Step 1: Create Datasource
    datasource = AtlasDatasource(project_name.lower() + '_datasource', 'admin', 'postgres.hostname.com',
                                 '5432', project_name.lower() + " demo csv file", contact_email)
    datasource_response = atlas_client.create_entity(datasource)
    datasource_guid = AtlasDatasource.extract_guid(datasource_response)
    print("datasource_guid : " + datasource_guid)

    # Step 2: Create Database
    database = AtlasDatabase(project_name.lower() + '_db', 'user', datasource_guid)
    database_response = atlas_client.create_entity(database)
    database_guid = AtlasDatabase.extract_guid(database_response)
    print("database_guid : " + database_guid)

    # Step 3: Create Table
    table = AtlasTable(project_name.lower() + '_table', 'user', database_guid)
    table_response = atlas_client.create_entity(table)
    table_guid = AtlasTable.extract_guid(table_response)
    print("table_guid : " + table_guid)

    # Step 4: Create Columns
    csv_columns = [AtlasColumn(name, 'user', table_guid, types[name], f"{name} column") for name in columns]
    column_response = atlas_client.create_bulk_entities(csv_columns)
    print("completed")


if __name__ == "__main__":
    main()
