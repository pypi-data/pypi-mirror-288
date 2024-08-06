from client import TrackTestRequest
from datetime import datetime

# Create an instance of TrackTestRequest
test_request = TrackTestRequest(
    name="ExampleIntegrationTest",
    trace="Trace data for debugging",
    executed_at=datetime.now(),
    result=True
)

# Define the API endpoint
api_endpoint = "http://localhost:8080/blueshell/trackTest"

# Send the test data to the API endpoint
response = test_request.send(api_endpoint)
print("Response Status Code:", response.status_code)
print("Response Body:", response.text)