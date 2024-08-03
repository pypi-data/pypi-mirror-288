# GenerativevalidationBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**body_object** | **object** |  | [optional] 
**prompt_key** | **str** | The key of the message that is being sent to the model. For example, \&quot;text\&quot; in the example for the object_body. Case sensitive. | [optional] 
**prompt_key_role** | **str** | The role that the prompt key should look for. If there is only one role, this can be omitted. Case sensitive. | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_body import GenerativevalidationBody

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationBody from a JSON string
generativevalidation_body_instance = GenerativevalidationBody.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationBody.to_json())

# convert the object into a dict
generativevalidation_body_dict = generativevalidation_body_instance.to_dict()
# create an instance of GenerativevalidationBody from a dict
generativevalidation_body_from_dict = GenerativevalidationBody.from_dict(generativevalidation_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

