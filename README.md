# Number Insight Async in Python

Very simple test application for the Number Insight API with Async responses, sometimes the Async response can contain more information as Nexmo can wait longer for responses from the carrier networks.

To make a request make GET with the number you want to looking eg `/get/447700900123` The initial response will be a 202 with the Nexmo API request ID however if you re-request after a ~30 seconds you will see the response data from Nexmo.
The application will return this data so long as its <180sec old, (we add a timestamp param the response data.

The responses are stored in a pickle file in `/files`
