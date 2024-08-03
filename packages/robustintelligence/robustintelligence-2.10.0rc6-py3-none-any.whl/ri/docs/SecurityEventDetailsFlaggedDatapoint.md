# SecurityEventDetailsFlaggedDatapoint


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**row_id** | **str** |  | [optional] 
**row_timestamp** | **datetime** |  | [optional] 

## Example

```python
from ri.apiclient.models.security_event_details_flagged_datapoint import SecurityEventDetailsFlaggedDatapoint

# TODO update the JSON string below
json = "{}"
# create an instance of SecurityEventDetailsFlaggedDatapoint from a JSON string
security_event_details_flagged_datapoint_instance = SecurityEventDetailsFlaggedDatapoint.from_json(json)
# print the JSON string representation of the object
print(SecurityEventDetailsFlaggedDatapoint.to_json())

# convert the object into a dict
security_event_details_flagged_datapoint_dict = security_event_details_flagged_datapoint_instance.to_dict()
# create an instance of SecurityEventDetailsFlaggedDatapoint from a dict
security_event_details_flagged_datapoint_from_dict = SecurityEventDetailsFlaggedDatapoint.from_dict(security_event_details_flagged_datapoint_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

