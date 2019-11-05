# Flask Endpoint Example
Flask is a Python web framework that can be used to implement or prototype web services very quickly.
This project demonstrates using the Flask web framework to implement a single, simple REST API endpoint.
 
The endpoint is `/message`. It accepts POST requests containg JSON data.

Request format:
```
{
   'id': number or string,
   'message': string
}
```

The endpoint returns JSON containing a count, indicating the number of words contained in the `message` fields of requests it has processed so far.
Requests with an `id` that has already been processed are ignored.

Response format:
```
{
   'count': number
}
```

All code for the endpoint is contained in `ExampleEndpoint.py`

## Prerequisites
This project was implemented and tested using the following:
* Ubuntu 18.04 LTS system (but it should run on other operating systems as well)
* Python 3.6.8
* Python 3 packages:
   * Flask==0.12.2
   * jsonschema==2.6.0

A `requirements.txt` is included for building a virtualenv environment, if necessary.

## Running the Automated Tests
A test driver, `test_endpoint.py`, is included for testing.
```
usage: test_endpoint.py [-h] [-i INPUT_FILE]

Sends requests to test endpoint.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        File to read test case data from (default:
                        ./test/test_data.json)
                       
```

Test data can be found in `test/`, along with a test data generation script, `test/generate_test_data.py`.
This script generates test data for 17 test cases and was used to generate the included `test/test_data.json` file.

```
usage: generate_test_data.py [-h] [-i INPUT_FILE] [-o OUTPUT_FILE]

Generates endpoint test data.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        File to select random words from (default:
                        /usr/share/dict/words)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        File to write output to (default:
                        ./test/test_data.json)
                       
```

The test driver reads the test cases and runs each on a fresh ExampleEndpoint instance. 
The test cases include requets to send, expected responses, and expected status codes. 

To run the test driver and execute the test cases, use the following:
```
python3 ./test_endpoint.py
```

You should see output similar to the following (shortened for brevity):
```
Running 17 tests..

== single_req_no_words ==
Result: PASS

== single_req_single_word ==
Result: PASS

   .. more tests ..

== malformed_message_field ==
Result: PASS

== extra_field ==
Result: PASS

==============================
 Tests passed: 17
 Tests failed: 0
==============================
```

## Running the Project Manually
Flask includes a built-in server for testing. This is what allows us to run the test suite above with real requests without a full-blown, production web server.

To run the project using the built-in test server, execute the following:
```
python3 ./ExampleEndpoint.py
```

You should see output similar to the following:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Requsts can be easily sent to the service using curl on the same machine. For example:
```
curl --data '{"id":0, "message": "This is a test"}' -H "Content-Type: application/json" -X POST http://localhost:5000/message
curl --data '{"id":1, "message": "Testing again"}'  -H "Content-Type: application/json" -X POST http://localhost:5000/message
curl --data '{"id":1, "message": "Duplicate ID"}'   -H "Content-Type: application/json" -X POST http://localhost:5000/message
```

Output of curl commands (responses from server):
```
{"count":4}
{"count":6}
{"count":6}
```

The Flask server indicates that it has successfully processed both requests:
```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [04/Nov/2019 21:08:56] "POST /message HTTP/1.1" 200 -
127.0.0.1 - - [04/Nov/2019 21:09:10] "POST /message HTTP/1.1" 200 -
127.0.0.1 - - [04/Nov/2019 21:10:29] "POST /message HTTP/1.1" 200 -
```


