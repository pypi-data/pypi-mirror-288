# RimeSyncImageTagResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image** | [**RimeManagedImage**](RimeManagedImage.md) |  | [optional] 
**job** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_sync_image_tag_response import RimeSyncImageTagResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeSyncImageTagResponse from a JSON string
rime_sync_image_tag_response_instance = RimeSyncImageTagResponse.from_json(json)
# print the JSON string representation of the object
print(RimeSyncImageTagResponse.to_json())

# convert the object into a dict
rime_sync_image_tag_response_dict = rime_sync_image_tag_response_instance.to_dict()
# create an instance of RimeSyncImageTagResponse from a dict
rime_sync_image_tag_response_from_dict = RimeSyncImageTagResponse.from_dict(rime_sync_image_tag_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

