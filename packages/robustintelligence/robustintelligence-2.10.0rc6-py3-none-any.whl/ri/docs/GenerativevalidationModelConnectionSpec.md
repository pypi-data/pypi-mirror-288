# GenerativevalidationModelConnectionSpec


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**http** | [**GenerativevalidationHttpConnectionSpec**](GenerativevalidationHttpConnectionSpec.md) |  | [optional] 
**bedrock** | [**GenerativevalidationBedrockConnectionSpec**](GenerativevalidationBedrockConnectionSpec.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_model_connection_spec import GenerativevalidationModelConnectionSpec

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationModelConnectionSpec from a JSON string
generativevalidation_model_connection_spec_instance = GenerativevalidationModelConnectionSpec.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationModelConnectionSpec.to_json())

# convert the object into a dict
generativevalidation_model_connection_spec_dict = generativevalidation_model_connection_spec_instance.to_dict()
# create an instance of GenerativevalidationModelConnectionSpec from a dict
generativevalidation_model_connection_spec_from_dict = GenerativevalidationModelConnectionSpec.from_dict(generativevalidation_model_connection_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

