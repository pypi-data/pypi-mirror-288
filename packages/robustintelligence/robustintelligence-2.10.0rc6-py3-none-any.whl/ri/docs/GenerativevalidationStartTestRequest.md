# GenerativevalidationStartTestRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Parameters for connecting to the user&#39;s generative model. | [optional] 
**http_headers** | **Dict[str, str]** |  | [optional] 
**endpoint_payload_template** | **str** | A string template that will be used to create the json payload sent to the LLM endpoint. This template must contain one and only one variable -- prompt_string. This will be replaced at runtime with the prompt used to send to the model. Used for arbitrary HTTP requests to models.  The template uses \&quot; and \&quot; as the opening and closing delimiters around the prompt_string variable name.  Example: &#39;{ \&quot;prompt\&quot;: \&quot;{{prompt_string}}\&quot; }&#39; Example: &#39;{ \&quot;message\&quot;: { \&quot;llm_prompt\&quot;: \&quot;{{prompt_string}}\&quot; } }&#39; | [optional] 
**response_json_path** | **str** | A json path specifying where in the HTTP response json payload we can find the LLM&#39;s response string. Note that the path must point to a string value in the json payload. Whitespace and other special characters can be encoded as unicode (\\u0020). Periods in json fields can be escaped with a backslash.  Example (top level field): - Endpoint response json: {\&quot;response\&quot;: \&quot;I am an AI Chatbot, how can I assist you?\&quot;} - response_json_path: \&quot;response\&quot;  Example (nested json field): - Endpoint response json: {\&quot;response\&quot;: {\&quot;llmResponse\&quot;: \&quot;I am an AI Chatbot, how can I assist you?\&quot;}} - response_json_path: \&quot;response.llmResponse\&quot;  Example (extract string from array): - Endpoint response: {\&quot;response\&quot;: {\&quot;options\&quot;: [\&quot;Hi\&quot;, \&quot;Hello there\&quot;], \&quot;count\&quot;: 2}} - response_json_path: \&quot;response.options.1\&quot;  Example (periods in field names): - Endpoint response: {\&quot;llm.response\&quot;: \&quot;hello\&quot;} - response_json_path: \&quot;llm\\\\.response\&quot;  The syntax uses dot notation only, such as \&quot;myfield.myotherfield\&quot; or \&quot;myarray.1\&quot;. | [optional] 
**http_auth_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**name** | **str** | The name to identify the generative model testing job. | [optional] 
**mutual_tls_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**system_prompt** | **str** | The system prompt that is currently active on the provided endpoint. | [optional] 
**aws_integration_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**model_id** | **str** | If aws_integration_id is set, this field will be the model id used for generative validation for bedrock. | [optional] 
**body** | [**GenerativevalidationBody**](GenerativevalidationBody.md) |  | [optional] 
**filters** | [**GenerativevalidationFilters**](GenerativevalidationFilters.md) |  | [optional] 
**workspace_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**agent_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.generativevalidation_start_test_request import GenerativevalidationStartTestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerativevalidationStartTestRequest from a JSON string
generativevalidation_start_test_request_instance = GenerativevalidationStartTestRequest.from_json(json)
# print the JSON string representation of the object
print(GenerativevalidationStartTestRequest.to_json())

# convert the object into a dict
generativevalidation_start_test_request_dict = generativevalidation_start_test_request_instance.to_dict()
# create an instance of GenerativevalidationStartTestRequest from a dict
generativevalidation_start_test_request_from_dict = GenerativevalidationStartTestRequest.from_dict(generativevalidation_start_test_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

