# maya-sdk
A client library for accessing Maya Insights API

## Usage

```python
import maya_sdk
maya_sdk.api_key = <API_KEY>
```

## API Key

Replace the <API_KEY> in the examples with an api key provided from Maya Insights. 

To generate a key, you could sign in to Maya on https://app.mayainsights.com on your business account (make sure you have received the invitation to join via email). From there, under Administration -> Developers you can find the API Key. 

Alternatively, contact our live chat support at https://mayainsights.com.

## Examples

### CSV Upload

```python
import maya_sdk
maya_sdk.api_key = <API_KEY>

with open("data.csv", "rb") as f:
    maya_sdk.files.upload_csv(category="imported_orders", file=f)
```

Feel free to adjust the category name to describe the data that is being sent.