# RimeCreateImageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image** | [**RimeManagedImage**](RimeManagedImage.md) |  | [optional] 
**job** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_create_image_response import RimeCreateImageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeCreateImageResponse from a JSON string
rime_create_image_response_instance = RimeCreateImageResponse.from_json(json)
# print the JSON string representation of the object
print(RimeCreateImageResponse.to_json())

# convert the object into a dict
rime_create_image_response_dict = rime_create_image_response_instance.to_dict()
# create an instance of RimeCreateImageResponse from a dict
rime_create_image_response_from_dict = RimeCreateImageResponse.from_dict(rime_create_image_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

