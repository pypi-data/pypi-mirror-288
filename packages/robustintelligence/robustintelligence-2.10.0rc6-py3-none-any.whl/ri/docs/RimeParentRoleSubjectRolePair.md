# RimeParentRoleSubjectRolePair

For users who have the specified role on the parent object, this specifies the role the user will have on the subject object (a child, such as a Project). For example, you can specify that a user with admin rights on a Workspace will get viewer rights on Projects in that Workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**subject_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 
**parent_role** | [**RimeActorRole**](RimeActorRole.md) |  | [optional] 

## Example

```python
from ri.apiclient.models.rime_parent_role_subject_role_pair import RimeParentRoleSubjectRolePair

# TODO update the JSON string below
json = "{}"
# create an instance of RimeParentRoleSubjectRolePair from a JSON string
rime_parent_role_subject_role_pair_instance = RimeParentRoleSubjectRolePair.from_json(json)
# print the JSON string representation of the object
print(RimeParentRoleSubjectRolePair.to_json())

# convert the object into a dict
rime_parent_role_subject_role_pair_dict = rime_parent_role_subject_role_pair_instance.to_dict()
# create an instance of RimeParentRoleSubjectRolePair from a dict
rime_parent_role_subject_role_pair_from_dict = RimeParentRoleSubjectRolePair.from_dict(rime_parent_role_subject_role_pair_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

