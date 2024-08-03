# RimeTimeInterval

TimeInterval describes a time interval.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **datetime** |  | [optional] 
**end_time** | **datetime** |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_time_interval import RimeTimeInterval

# TODO update the JSON string below
json = "{}"
# create an instance of RimeTimeInterval from a JSON string
rime_time_interval_instance = RimeTimeInterval.from_json(json)
# print the JSON string representation of the object
print(RimeTimeInterval.to_json())

# convert the object into a dict
rime_time_interval_dict = rime_time_interval_instance.to_dict()
# create an instance of RimeTimeInterval from a dict
rime_time_interval_from_dict = RimeTimeInterval.from_dict(rime_time_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

