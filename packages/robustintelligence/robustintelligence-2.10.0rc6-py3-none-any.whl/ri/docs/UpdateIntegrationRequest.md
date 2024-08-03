# UpdateIntegrationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**integration** | [**UpdateIntegrationRequestIntegration**](UpdateIntegrationRequestIntegration.md) |  | [optional] 
**mask** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.update_integration_request import UpdateIntegrationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateIntegrationRequest from a JSON string
update_integration_request_instance = UpdateIntegrationRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateIntegrationRequest.to_json())

# convert the object into a dict
update_integration_request_dict = update_integration_request_instance.to_dict()
# create an instance of UpdateIntegrationRequest from a dict
update_integration_request_from_dict = UpdateIntegrationRequest.from_dict(update_integration_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

