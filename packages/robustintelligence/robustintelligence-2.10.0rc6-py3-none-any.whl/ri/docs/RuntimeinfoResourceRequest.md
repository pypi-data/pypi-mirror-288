# RuntimeinfoResourceRequest

Specifies Kubernetes resource requests for a Stress Test Job.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ram_request_megabytes** | **str** | Megabytes of RAM requested for the Stress Test Job. | [optional] 
**cpu_request_millicores** | **str** | Millicores of CPU requested for the Stress Test Job. | [optional] 

## Example

```python
from ri.apiclient.models.runtimeinfo_resource_request import RuntimeinfoResourceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RuntimeinfoResourceRequest from a JSON string
runtimeinfo_resource_request_instance = RuntimeinfoResourceRequest.from_json(json)
# print the JSON string representation of the object
print(RuntimeinfoResourceRequest.to_json())

# convert the object into a dict
runtimeinfo_resource_request_dict = runtimeinfo_resource_request_instance.to_dict()
# create an instance of RuntimeinfoResourceRequest from a dict
runtimeinfo_resource_request_from_dict = RuntimeinfoResourceRequest.from_dict(runtimeinfo_resource_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

