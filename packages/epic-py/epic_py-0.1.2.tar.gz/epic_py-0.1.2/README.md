# epic-py package

This is the Python client for ePIC API `version >= 3.0.0`.

## Features

### Get a PID

To get a PID and its values, simply call the `get` method. It returns a `Pid` object which contains `prefix`, `suffix`,
and its values in `data` variable. Note that if `username` and `password` are not provided, the client can only get the
PID and its public readable values.

### Create a PID

To create a PID, a `Pid` object must first be created with proper `data`, which is a list of `PidData` (handle values).
Please see the example usage below for more details.

There are 2 ways to create a PID:

1. Call the `create` method: this method will throw an error in case the PID has already existed.
1. Call the `create_or_update` method: as the name suggested, if the PID has already existed, it will be updated
   instead. This update overwrites the PID with new data.

### Update a PID

To update a PID, a `Pid` object must first be created with proper `prefix`, `suffix`, and `data`. `data` is a list
of `PidData` (handle values).

Same as create, there are 2 ways to update a PID:

1. Call the `update` method: this method will throw an error in case the PID does not exist.
1. Call the `create_or_update` method: if the PID already exists, it will be updated. This update overwrites the PID
   with new data.

### Delete a PID

To delete a PID, simply call the `delete` method and pass the PID string as a parameter. This command does not guarantee
that the PID will be deleted. It depends on the policies of each prefix. Usually, the `no-delete` policy is enforced. If
that is the case, trying to delete a PID will lead to an error.

## Example usage

Suppose one wants to create a PID with its content as follows:

```json
[
  {
    "parsed_data": "Test Publisher",
    "type": "publisher"
  },
  {
    "parsed_data": "2021",
    "type": "publicationYear",
    "privs": "rw--"
  },
  {
    "parsed_data": {
      "identifier-Attribute": "DOI",
      "identifier-Value": "10.123.456/789"
    },
    "type": "identifier"
  },
  {
    "parsed_data": {
      "resourceType-Value": "test"
    },
    "type": "resourceType"
  },
  {
    "parsed_data": {
      "creator": {
        "creatorName": "Triet Doan"
      }
    },
    "type": "creators"
  },
  {
    "parsed_data": {
      "title": {
        "title-Value": "Test title"
      }
    },
    "type": "titles"
  }
]
```

The following example code can be used:

```python
from epic_py import EpicAPI, PidData, Pid

publisher = PidData(type='publisher', parsed_data='Test Publisher')
publication_year = PidData(type='publicationYear', parsed_data='2021', privs='rw--')
identifier = PidData(type='identifier',
                     parsed_data={"identifier-Attribute": "DOI", "identifier-Value": "10.123.456/789"})
resource_type = PidData(type='resourceType', parsed_data={"resourceType-Value": "test"})
creators = PidData(type='creators', parsed_data={"creator": {"creatorName": "Triet Doan"}})
titles = PidData(type='titles', parsed_data={"title": {"title-Value": "Test title"}})

# Create the PID object
prefix = 'my_prefix'
pid = Pid(prefix=prefix, data=[publisher, publication_year, identifier, resource_type, creators, titles])

# Create the client
epic_api = EpicAPI('<host>', '<username>', '<password>')

# Create the PID
pid = epic_api.create(pid)

# Get the PID
pid_response = epic_api.get(pid.pid_str)

# Delete the PID
epic_api.delete(pid.pid_str)
```