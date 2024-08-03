# ValidateResponseProcessedRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_id** | **str** | Unique identifier of the request. | [optional] 
**user_input_text** | **str** | Information about the &#x60;user_input_text&#x60;. The raw input is truncated if it exceeds a certain token length so we do not denial of service downstream logging and data systems. | [optional] 
**input_token_count** | **int** |  | [optional] 
**contexts** | **List[str]** | Information about the &#x60;contexts&#x60;. The contexts are truncated if it exceeds a certain token length so we do not denial of service downstream logging and data systems. | [optional] 
**contexts_token_count** | **int** |  | [optional] 
**output_text** | **str** | Information about the &#x60;output_text&#x60;. The output text is truncated if it exceeds a certain token length so we do not denial of service downstream logging and data systems. | [optional] 
**output_token_count** | **int** |  | [optional] 

## Example

```python
from ri.fwclient.models.validate_response_processed_request import ValidateResponseProcessedRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateResponseProcessedRequest from a JSON string
validate_response_processed_request_instance = ValidateResponseProcessedRequest.from_json(json)
# print the JSON string representation of the object
print(ValidateResponseProcessedRequest.to_json())

# convert the object into a dict
validate_response_processed_request_dict = validate_response_processed_request_instance.to_dict()
# create an instance of ValidateResponseProcessedRequest from a dict
validate_response_processed_request_from_dict = ValidateResponseProcessedRequest.from_dict(validate_response_processed_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

