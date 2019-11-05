#!/usr/bin/env python3

import json
import random
import argparse

from ExampleEndpoint import ExampleEndpoint 


def run_test(test_name, test_data):
   """
   Creates an ExampleEndpoint object and executes a single test case on it.
   
   Parameters:
      test_name:  Name of this test as a string
      test_data:  Dict containing the test data: 
                     requests: list of JSON requests to send
                     status:   expected status code at end of test  
                     count:    expected count returned at end of test
   Returns:
      bool:       Whether this test passed or not
   """

   endpoint = ExampleEndpoint()
   test_client = endpoint.get_test_client()
   
   response = None
   
   # send each request to the endpoint using the test client
   for request in test_data['requests']:
      response = test_client.post('/message', data=json.dumps(request), content_type='application/json')
   
   expected_status_code = test_data['status']

   test_pass = True
   
   if response.status_code != expected_status_code:
      test_pass = False
      print ("Expected {} response code got {}".format(expected_status_code, response.status_code))
   
   # only check the response data if this is a happy path test and the test is currently passing
   if expected_status_code == 200 and test_pass:
      json_data = json.loads(response.data)
   
      count = json_data['count']
   
      if count != test_data['count']:
         test_pass = False
         print ("Expected {} got {}".format(test_data['count'], count))
         
   print_test_results(test_name, test_pass)
   
   return test_pass


def print_test_results(test_name, test_pass):
   print ("== {} ==".format(test_name))         
   print ("Result: ", end='')
   print ("PASS") if test_pass else print ("FAIL")
   print()
      
      
if __name__ == "__main__":
   arg_parser = argparse.ArgumentParser(description="Sends requests to test endpoint.", 
                                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
   arg_parser.add_argument('-i', '--input_file', 
                           help="File to read test case data from",
                           default='./test/test_data.json')
                        
   args = arg_parser.parse_args()

   with open(args.input_file, 'r') as infile:
      tests = json.load(infile)
      
   print ("Running {} tests..\n".format(len(tests.keys())))
   
   results = []
   
   for test_name, test_data in tests.items():  
      results.append(run_test(test_name, test_data))
      
   passed = results.count(True)
   failed = results.count(False)
   
   print ("==============================")
   print (" Tests passed: {}".format(passed))
   print (" Tests failed: {}".format(failed))
   print ("==============================")


