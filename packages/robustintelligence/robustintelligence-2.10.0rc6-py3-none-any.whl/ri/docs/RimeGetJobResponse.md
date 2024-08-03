# RimeGetJobResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**job** | [**RimeJobMetadata**](RimeJobMetadata.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_get_job_response import RimeGetJobResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RimeGetJobResponse from a JSON string
rime_get_job_response_instance = RimeGetJobResponse.from_json(json)
# print the JSON string representation of the object
print(RimeGetJobResponse.to_json())

# convert the object into a dict
rime_get_job_response_dict = rime_get_job_response_instance.to_dict()
# create an instance of RimeGetJobResponse from a dict
rime_get_job_response_from_dict = RimeGetJobResponse.from_dict(rime_get_job_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

