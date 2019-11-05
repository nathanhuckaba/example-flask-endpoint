#!/usr/bin/env python3

import flask 
import json
import jsonschema

class ExampleEndpoint(object):
   """
   Simple Flask endpoint that accepts JSON POST requests containing the fields id and message.
   
   The id field should contain the request identifier (strings and integers are accepted).
   The message field should be a string containing zero or more words. 
   
   The number of words processed by the application since startup is returned as a response 
   to each request. Requests containing an id that has already been processed will be ignored.
   
   Attributes:
      processed_ids: A dict to store ids that have been processed previously
      word_count:    Running total of number of words contained in processed requests
      app:           Flask object that handles incoming requests
   """
   
   def __init__(self):
      # dict to store ids that have been processed since application began running
      # dict is used due to its fast O(1) lookups
      self.processed_ids = {}

      # running total of words processed in 'message' field of requests
      self.word_count = 0
      
      self.app = flask.Flask(__name__)
      self.app.add_url_rule('/message', 'process_message', self.process_message, methods=['POST'])  
      
      
   def parse_post_request(self, request_data):
      """ 
      Parses the given request data as JSON and validates it against the expected reqeust schema
      
      Parameters:
         request_data: Dict containing the request data
         
      Returns:
         bool: whether or not the request was valid
         int:  id field
         str:  message field
      """
       
      schema = {
                  "type": "object",
                  
                  "properties": {
                     "id": {
                        "type": ["string", "number"]
                     },
                     
                     "message": {
                        "type": "string"
                     }
                  },

                  "required": ["id", "message"],
                  "additionalProperties": False
               }
                     
      request_valid = True

      request_id = None
      request_message = None

      try:
         jsonschema.validate(instance=request_data, schema=schema)
   
         request_id = request_data['id']
         request_message = request_data['message']
   
      except jsonschema.exceptions.ValidationError:
         request_valid = False
      
      return request_valid, request_id, request_message
      
      
   def process_message(self):
      """ 
      Flask view function. 
      Process a client request and returns the current word total to the client.
      """
   
      if not flask.request.is_json:
          flask.abort(400, "Invalid content type. Expected JSON data.")
      
      # will return None if parsing failed
      request_data = flask.request.get_json(silent=True)

      if request_data is None:
         flask.abort(400, "Failed to parse JSON data. Check data format.")

      # extract fields from request and validate against schema
      request_valid, request_id, request_message = self.parse_post_request(request_data)

      # if request is not valid, stop processing and send back a 400 Bad Request with informative error message
      if not request_valid:
         flask.abort(400, "Expected JSON data containing two fields: id, message")

      # treat all ids as strings (allowing non-numeric ids)
      # note that this causes number ids and their associated string ids to be equivalent (i.e. 25 and '25')
      request_id = str(request_id)

      # only process this request if its id has not been processed previously
      if self.processed_ids.get(request_id, False) == False:

         # mark this request id as processed
         self.processed_ids[request_id] = True

         # split the message field into words (handles single as well as multiple spaces b/w words)
         # add the word count of this message to the running total
         self.word_count += len(request_message.split())

      # return the running total response with a status code of 200 OK
      # jsonify will set the appropriate Content-Type in the response
      return flask.jsonify({'count': self.word_count}), 200


   def run(self):
      """Start accepting requests"""
      
      # explicitly disable multi-threading (recent versions of flask are multi-threaded by default) 
      # also, explicitly set number of processes to 1
      self.app.run(threaded=False, processes=1) 
      
      # Supporting multiple threads would involve adding locking to ensure correctness. Without 
      # locking, two requests with the same id could make it past the duplicate id check before 
      # either is added to the processed ids list.

      # Supporting multiple processes would involve providing a way for all of the processes to 
      # operate on the same persistent data. This would most likely be solved by using a database 
      # to store request ids and word counts. Care would need to be taken to ensure that checking 
      # if an id has been processed and setting it as processed is an atomic transaction.
   
   
   def get_test_client(self):
      """Return a test client that can be used for unit testing"""
      return self.app.test_client()
      
      
if __name__ == "__main__":
   endpoint = ExampleEndpoint()
   endpoint.run()

