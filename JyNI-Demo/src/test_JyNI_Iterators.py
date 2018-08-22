'''
 * Copyright of JyNI:
 * Copyright (c) 2013, 2014, 2015, 2016, 2017 Stefan Richthofer.
 * All rights reserved.
 *
 *
 * Copyright of Python and Jython:
 * Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
 * 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017
 * Python Software Foundation.
 * All rights reserved.
 *
 *
 * This file is part of JyNI.
 *
 * JyNI is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * JyNI is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with JyNI.  If not, see <http://www.gnu.org/licenses/>.


Created on: 2018-08-07 16:21

@author: Calum Freeman
'''
import sys
import os
import platform
from pickletools import string1
from unittest.case import SkipTest

if os.name == 'java':
	systm = platform.java_ver()[-1][0].lower().replace(' ', '')
	if systm == 'macosx':
		ver = platform.java_ver()[-1][1]
		ver = ver[:5] # e.g."10.12.4" => "10.12"
		buildf = '-'.join((systm, ver, 'intel'))
	else:
		if systm.startswith('win'):
			systm = 'win'
		buildf = '-'.join((systm, os.uname()[-1]))
else:
	systm = os.uname()[0].lower()
	if systm == 'darwin':
		ver = platform.mac_ver()[0]
		ver = ver[:5] # e.g."10.12.4" => "10.12"
		buildf = '-'.join(('macosx', ver, 'intel'))
	else:
		buildf = '-'.join((systm, os.uname()[-1]))


#Since invalid paths do no harm, we add several possible paths here, where
#PyFileTest.so could be located in various build scenarios. If you use different
#scenarios in parallel, select the one to be used by setting some of the paths as comments.

#built with an IDE in debug mode:
sys.path.append('../../DemoExtension/Debug') #in case you run it from src dir
sys.path.append('./DemoExtension/Debug') #in case you run it from base dir
#built with an IDE in release mode:
sys.path.append('../../DemoExtension/Release') #in case you run it from src dir
sys.path.append('./DemoExtension/Release') #in case you run it from base dir
sys.path.append('../../DemoExtension/build/Release') #in case you run it from src dir
sys.path.append('./DemoExtension/build/Release') #in case you run it from base dir
#built with setup.py:
sys.path.append('../../DemoExtension/build/lib.'+buildf+'-2.7') #in case you run it from src dir
sys.path.append('./DemoExtension/build/lib.'+buildf+'-2.7') #in case you run it from base dir
sys.path.append('./DemoExtension/build')
import datetime
import unittest
import IteratorsTest as it

class TestIterators(unittest.TestCase):
	
	def test_iternext(self):
		dictionary = dict(one=1, two=2, three=3, four=4, five=5)
		python_iterator = dictionary.__iter__()
		number_of_iterations = 3
		for i in range(0, number_of_iterations):
			python_result = python_iterator.next()
		c_extension_result = it.test_iternext(dictionary, number_of_iterations)
		self.assertEqual(python_result, c_extension_result)
	
	def test_tp_as_sequence_sq_contains(self):
		dictionary = dict(one=1, two=2, three=3, four=4, five=5)
		key = "two"
		c_extension_result = it.test_tp_as_sequence_sq_contains(dictionary, key)
		self.assertTrue(c_extension_result)
		
	def test_tp_as_mapping_mp_length(self):
		dictionary = dict(one=1, two=2, three=3, four=4, five=5)
		length = it.test_tp_as_mapping_mp_length(dictionary)
		self.assertEqual(length, len(dictionary))
	
	def test_tp_as_mapping_mp_subscript(self):
		dictionary = dict(one=1, two=2, three=3, four=4, five=5)
		key = "two"
		value = it.test_tp_as_mapping_mp_subscript(dictionary, key)
		self.assertEqual(dictionary[key], value)
	
	def test_tp_as_mapping_mp_ass_subscript(self):
		dictionary = dict(one=1, two=2, three=3, four=4, five=5)
		key = "two"
		new_value = 6
		it.test_tp_as_mapping_mp_ass_subscript(dictionary, key, new_value)
		self.assertEqual(dictionary[key], new_value)
	
	def test_nprand(self):
		import numpy as np
		# generate x random integers between 0 and y and count how many you get of each
		x = 10000
		y = 10
		out = [0]*y
		for i in range(x):
			out[np.random.randint(y)] += 1
		# work out the mean and standard deviation of the sample
		mean = np.mean(out)
		sigma = 0
		for i in range(len(out)):
			sigma += ((out[i]-mean)**2)/(len(out)+1)
		import math
		sigma = math.sqrt(sigma)
		# make sure nothing statistically significant happened
		self.assertGreater(3, (max(out)-mean)/sigma, "randint generated a non-random sample, try re-running the test as it could be a fluke")
		self.assertGreater(3, (mean-min(out))/sigma, "randint generated a non-random sample, try re-running the test as it could be a fluke")



if __name__ == '__main__':
	# This code can be commented in/out to allow individual tests to be ran
	#suite = unittest.TestLoader().loadTestsFromName("test_nprand", TestIterators)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_iternext", TestIterators)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_tp_as_mapping_mp_length", TestIterators)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_tp_as_mapping_mp_subscript", TestIterators)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_tp_as_mapping_mp_ass_subscript", TestIterators)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	unittest.main()