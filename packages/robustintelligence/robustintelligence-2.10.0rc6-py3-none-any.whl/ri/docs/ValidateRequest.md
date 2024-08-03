# ValidateRequest

ValidateRequest is a single request to the firewall on a piece of user input / output. Either the input or output must be provided.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_input_text** | **str** | Input text is the raw user input. The generative firewall performs validation on input to prevent risk configured by firewall rules. | [optional] 
**contexts** | **List[str]** | Documents that represent relevant context for the input query that is fed into the model. e.g. in a RAG application this will be the documents loaded during the RAG Retrieval phase to augment the LLM&#39;s response. | [optional] 
**output_text** | **str** | Output text is the raw output text of the model. The generative firewall performs validation on the output so the system can determine whether to show it to users. | [optional] 
**firewall_instance_id** | **object** | Unique ID of an object in RIME. | [optional] 

## Example

```python
from ri.fwclient.models.validate_request import ValidateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateRequest from a JSON string
validate_request_instance = ValidateRequest.from_json(json)
# print the JSON string representation of the object
print(ValidateRequest.to_json())

# convert the object into a dict
validate_request_dict = validate_request_instance.to_dict()
# create an instance of ValidateRequest from a dict
validate_request_from_dict = ValidateRequest.from_dict(validate_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

