# RimeGetImageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**image** | [**RimeManagedImage**](RimeManagedImage.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_image_response import RimeGetImageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetImageResponse from a JSON string
rime_get_image_response_instance = RimeGetImageResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetImageResponse.to_json())

# convert the object into a dict
rime_get_image_response_dict = rime_get_image_response_instance.to_dict()
# create an instance of RimeGetImageResponse from a dict
rime_get_image_response_from_dict = RimeGetImageResponse.from_dict(rime_get_image_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

