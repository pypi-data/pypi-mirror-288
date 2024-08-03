# RimeUUID

Unique ID of an object in RIME.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** | Unique object ID. | [optional] 

## Example

```python
from ri.fwclient.models.rime_uuid import RimeUUID

# TODO update the JSON string below
json = "{}"
# create an instance of RimeUUID from a JSON string
rime_uuid_instance = RimeUUID.from_json(json)
# print the JSON string representation of the object
print(RimeUUID.to_json())

# convert the object into a dict
rime_uuid_dict = rime_uuid_instance.to_dict()
# create an instance of RimeUUID from a dict
rime_uuid_from_dict = RimeUUID.from_dict(rime_uuid_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

