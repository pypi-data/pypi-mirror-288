# RegistryDatabricksInfo

DatabricksInfo provides the information needed to load a Delta Lake table from Databricks.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**table_name** | **str** | The database table name to use. | 

## Example

```python
from ri.apiclient.models.registry_databricks_info import RegistryDatabricksInfo

# TODO update the JSON string below
json = "{}"
# create an instance of RegistryDatabricksInfo from a JSON string
registry_databricks_info_instance = RegistryDatabricksInfo.from_json(json)
# print the JSON string representation of the object
print(RegistryDatabricksInfo.to_json())

# convert the object into a dict
registry_databricks_info_dict = registry_databricks_info_instance.to_dict()
# create an instance of RegistryDatabricksInfo from a dict
registry_databricks_info_from_dict = RegistryDatabricksInfo.from_dict(registry_databricks_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

