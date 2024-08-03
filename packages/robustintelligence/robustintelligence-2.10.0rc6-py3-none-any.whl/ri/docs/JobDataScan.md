# JobDataScan

A file scan job runs over a registered model. It is used to assess a model's supply chain security risk.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_id** | [**RimeUUID**](RimeUUID.md) |  | [optional] 
**file_scan_id** | **str** |  | [optional] 

## Example

```python
from ri.apiclient.models.job_data_scan import JobDataScan

# TODO update the JSON string below
json = "{}"
# create an instance of JobDataScan from a JSON string
job_data_scan_instance = JobDataScan.from_json(json)
# print the JSON string representation of the object
print(JobDataScan.to_json())

# convert the object into a dict
job_data_scan_dict = job_data_scan_instance.to_dict()
# create an instance of JobDataScan from a dict
job_data_scan_from_dict = JobDataScan.from_dict(job_data_scan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

