# RimeGetURLResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | [**RimeSafeURL**](RimeSafeURL.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_url_response import RimeGetURLResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetURLResponse from a JSON string
rime_get_url_response_instance = RimeGetURLResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetURLResponse.to_json())

# convert the object into a dict
rime_get_url_response_dict = rime_get_url_response_instance.to_dict()
# create an instance of RimeGetURLResponse from a dict
rime_get_url_response_from_dict = RimeGetURLResponse.from_dict(rime_get_url_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

