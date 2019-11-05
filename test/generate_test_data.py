#!/usr/bin/env python3

import json
import random
import argparse

   
class TestDataGenerator(object):
   """ 
   Class to assist in the generation of test data for our example endpoint.
   """
   
   def __init__(self, word_file):
      """Load the input word file for use during test generation"""
      try:
         with open(word_file) as input_word_file:
            words = input_word_file.read().splitlines()
         
      except:
         print ("ERROR: could not open the input word file.")
         raise
      
      self.words = words
      

   def create_manual_test_case(self, request, status_code, count=None):
      """
      Generates JSON for a test case containing a manually created request.
      
      Parameters:
         request:       Dict representing the JSON request.
         status_code:   Expected status code request will cause.
         count:         Expected count field of response (omit for error cases).
         
      Returns:
         dict:          JSON representation of this test case
      """
      
      test_data = {
                     'requests': [request],  
                     'count': count, 
                     'status': status_code
                  }

      if count is None:
         test_data.pop('count')
      
      return test_data
      
      
   def gen_test_case(self, num_requests, num_words=[], ids=None, uniform_spacing=True):
      """
      Generates a test case for our example endpoint.
      
      Parameters:
         num_requests:     Number of requests to generate for this test case.
         num_words:        List indicating number of words per request.
                              Set to scalar to use the same for all. 
                              Omit to use a random number [2, 10] for all.
         ids:              List of ids to use for the requests (omit to use default of 0..n).
         uniform_spacing:  Bool indicating whether spacing should be uniform (1 space) or randomized.
         
      Returns:
         dict:             JSON representation of this test case
      """
      
      if type(num_words) is not list:
         num_words = [num_words] * num_requests 
         
      if len(num_words) == 0:
         # 2 to 10 words per request
         num_words = random.choices(range(2,11), k=num_requests)
      
      if ids is None:
         # default to simple, non-repeating ids if none are given
         ids = [i for i in range(num_requests)]
      
      requests = []
      
      word_counts = {}
      
      for req_idx in range(num_requests):
         message_field = ''
         num_words_this_req = num_words[req_idx]
         
         for _ in range (num_words_this_req):
            spacing = " "
            
            # if enabled, use a random amount of spacing b/w words      
            if not uniform_spacing:
               spacing *= random.randint(1, 5)
               
            message_field += random.choice(self.words) + spacing 
         
         this_req_id = ids[req_idx]
         
         requests.append({'id': this_req_id, 'message': message_field.strip()})
         
         if word_counts.get(this_req_id) is None:
            word_counts[this_req_id] = num_words_this_req
            
      return {'requests': requests, 'count': sum(word_counts.values()), 'status': 200}


if __name__ == "__main__":
   arg_parser = argparse.ArgumentParser(description="Generates endpoint test data.",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   
   # Note: /usr/share/dict/words includes some words containing Unicode characters, this should be fine 
   arg_parser.add_argument('-i', '--input_file', 
                           help="File to select random words from",
                           default='/usr/share/dict/words')
                           
   arg_parser.add_argument('-o', '--output_file', 
                           help="File to write output to",
                           default='./test_data.json')
                           
   args = arg_parser.parse_args()

   word_file = args.input_file
   out_file  = args.output_file
   
   tdg = TestDataGenerator(word_file)
   
   testdata = {}      

   # happy path tests
   testdata['single_req_no_words'] = tdg.gen_test_case(num_requests=1, num_words=[0])
   
   testdata['single_req_single_word']     = tdg.gen_test_case(num_requests=1, num_words=[1])
   testdata['single_req_multiple_words']  = tdg.gen_test_case(num_requests=1, num_words=[5])

   testdata['single_req_multiple_words_random_spacing'] = tdg.gen_test_case(num_requests=1, num_words=[20], uniform_spacing=False)

   testdata['multiple_req_single_word']   = tdg.gen_test_case(num_requests=5, num_words=1)
   testdata['multiple_req_multiple_word'] = tdg.gen_test_case(num_requests=10)

   testdata['non_unique_ids_1'] = tdg.gen_test_case(num_requests=3, ids=[1, 1, 1])
   testdata['non_unique_ids_2'] = tdg.gen_test_case(num_requests=3, ids=[2, 1, 1])
   testdata['non_unique_ids_3'] = tdg.gen_test_case(num_requests=3, ids=[1, 2, 1])
   testdata['non_unique_ids_4'] = tdg.gen_test_case(num_requests=3, ids=[1, 1, 2])
   
   # manually add some tests that produce error conditions
   testdata['invalid_json'] = tdg.create_manual_test_case(request="invalid", status_code=400)
   
   testdata['empty_request']    = tdg.create_manual_test_case(request={},                   status_code=400)
   testdata['no_id_field']      = tdg.create_manual_test_case(request={'message': 'test'},  status_code=400)
   testdata['no_message_field'] = tdg.create_manual_test_case(request={'id': 0},            status_code=400)
   
   testdata['malformed_id_field']      = tdg.create_manual_test_case(request={'id': False, 'message': ''},    status_code=400)
   testdata['malformed_message_field'] = tdg.create_manual_test_case(request={'id': 0,     'message': False}, status_code=400)
   
   testdata['extra_field'] = tdg.create_manual_test_case(request={'id': 0, 'message': 'test', 'extra': 0}, status_code=400)
   
   # write the test data to file
   with open(out_file, 'w') as outfile:
      json.dump(testdata, outfile, indent=3)
   


