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


Created on: 2018-07-30 13:35

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
import PyFileTest as pf

class TestPyFile(unittest.TestCase):
	
	def setUp(self):
		# TODO check if the file exists, if it does pick a different one from a list of names(if no file can be made raise an exception). Make sure it and any other files are removed by the end.
		self.name = "/tmp/JyNI_tests"
		self.mode = "w+"
		self.file = open(self.name, self.mode)
	
	def tearDown(self):
		self.file.close()
		import os
		os.remove(self.name)
	
	def test_PyFile_WriteString(self): # TODO assertRaises() would allow testing exceptions if we add an exception for null file
		string = "Hello World!"
		self.assertEqual(pf.test_PyFile_WriteString(self.file, string), 1)
		self.file.close()
		self.file = open(self.name, 'r+')
		res = self.file.read()
		self.assertEqual(res, string, "failed to write: \""+str(string)+"\" to file, got: \""+res+"\" instead");
	
	def test_PyFile_AsFile(self):
		string = 'a'
		self.file.write(string)
		self.file.close()
		self.file = open(self.name, 'r+') 
		self.assertEqual(pf.test_PyFile_AsFile(self.file, string), string)
		self.file.close()
		self.assertEqual(pf.test_PyFile_AsFile(self.file, string), "file is closed")
	
	def test_PyFile_Name(self):
		self.assertEqual(pf.test_PyFile_Name(self.file), self.name)
	
	def test_PyFile_FromFile(self): # Note: this assumes that PyFile_AsFile works!
		# TODO find a better way to test this
		self.file2 = pf.test_PyFile_FromFile(self.file, self.name, "w+")
		self.assertEqual(self.file.mode, self.file2.mode, "PyFile_FromFile gave file with different self.mode")
		self.assertEqual(self.file.name, self.file2.name, "PyFile_FromFile gave file with different self.name")
	
	def test_PyFile_FromString(self): # Note: this assumes that PyFile_AsFile works!
		# TODO find a better way to test this
		self.file2 = pf.test_PyFile_FromString(self.name, "w+")
		self.assertEqual(self.file.mode, self.file2.mode, "PyFile_FromFile gave file with different self.mode")
		self.assertEqual(self.file.name, self.file2.name, "PyFile_FromFile gave file with different self.name")
	
	def test_PyFile_GetLine(self):
		one = "Hello\n"
		two = "World\n"
		three = "Testing GetLine\n"
		self.file.write(one)
		self.file.write(two)
		self.file.write(three)
		self.file.close()
		self.file = open(self.name, "r+")
		onef = pf.test_PyFile_GetLine(self.file, -1)
		twof = pf.test_PyFile_GetLine(self.file, -1)
		threef = pf.test_PyFile_GetLine(self.file, -1)
		self.assertEqual(one, onef)
		self.assertEqual(two, twof)
		self.assertEqual(three, threef)
		
	def test_PyFile_SetBufSize(self):
		pf.test_PyFile_SetBufSize(self.file, 404) # Just checking it doesn't throw an error, the method doesn't do anything
		
	def test_PyFile_SetEncoding(self):
		enc = "hello?";
		pf.test_PyFile_SetEncoding(self.file, enc)
		self.assertEqual(self.file.encoding, enc)
		
	def test_PyFile_SetEncodingAndErrors(self):
		enc = "hello";
		err = "world?";
		pf.test_PyFile_SetEncodingAndErrors(self.file, enc, err)
		self.assertEqual(self.file.encoding, enc)
		self.assertEqual(self.file.errors, err)
		
	def test_PyFile_SoftSpace(self):
		# Note: all positive integers will be treated as 1 by softspace(It's really a boolean)
		pf.test_PyFile_SoftSpace(self.file, 1)
		# the flag should be set to 1, so when the old flag is returned it should be 1
		self.assertEqual(1, pf.test_PyFile_SoftSpace(self.file, 0))
		# Now the old flag should be 0
		self.assertEqual(0, pf.test_PyFile_SoftSpace(self.file, 1))
	
	def test_PyFile_Check(self):
		self.assertFalse(pf.test_PyFile_Check([1,2]))
		self.assertTrue(pf.test_PyFile_Check(self.file))
	
	def test_PyFile_CheckExact(self):
		self.assertFalse(pf.test_PyFile_CheckExact([1,2]))
		self.assertTrue(pf.test_PyFile_CheckExact(self.file))
		
	def test_PyFile_IncUseCount(self):
		pf.test_PyFile_IncUseCount(self.file)
		
	def test_PyFile_DecUseCount(self):
		pf.test_PyFile_DecUseCount(self.file)
	
	def test_PyFile_WriteObject(self):
		def check(Object):
			thing = pf.test_PyFile_WriteObject(self.file, Object, 0)
			self.assertEqual(thing, 0, "Error while writing object to file")
			self.file.write("\n")
			self.file.close()
			self.file = open(self.name, "r")
			self.assertEqual(self.file.read(), str(Object)+"\n")
			self.file = open(self.name, self.mode)
		check(4)
		check([2,3])
		# some weird object should also be checked
	
	def test_PyObject_AsFileDescriptor(self):
		self.assertEqual(pf.test_PyObject_AsFileDescriptor(4), 4)
		self.assertEqual(pf.test_PyObject_AsFileDescriptor(4.4), -1)
		self.assertEqual(pf.test_PyObject_AsFileDescriptor(self.file), int(self.file.fileno()))
		
	def test_tp_dealloc(self):
		#print pf.test_tp_dealloc(self.file)
		raise(Exception("Not yet Implemented"))
		
	def test_tp_repr(self):
		self.assertEqual(str(self.file), pf.test_tp_repr(self.file))
	
	def test_tp_getattro(self):
		# Checks it can get things from file_getsetlist
		self.assertFalse(pf.test_tp_getattro(self.file, "closed"))
		# Checks it can get things from file_methods
		pf.test_tp_getattro(self.file, "close")()
		self.assertTrue(pf.test_tp_getattro(self.file, "closed"))   
		# Checks it can get things from file_memberlist
		self.assertEqual(pf.test_tp_getattro(self.file, "name"), self.name)
	
	def test_tp_setattro(self): # relies on tp_getattro working
		# Checks it can get things from file_memberlist
		s = 1
		pf.test_tp_setattro(self.file, "softspace", s)
		self.assertEqual(pf.test_tp_getattro(self.file, "softspace"), s)
		s = 0
		pf.test_tp_setattro(self.file, "softspace", s)
		self.assertEqual(pf.test_tp_getattro(self.file, "softspace"), s)
	
	def test_tp_weaklistoffset(self):
		raise(Exception("Not yet Implemented"))
	
	def test_file_memberlist(self): # relies on PyFile_SetEncodingAndErrors and tp_getattro working
		self.assertEqual(pf.test_tp_getattro(self.file, "mode"), self.mode)
		self.assertEqual(pf.test_tp_getattro(self.file, "name"), self.name)
		enc = "hello";
		err = "world?";
		pf.test_PyFile_SetEncodingAndErrors(self.file, enc, err)
		self.assertEqual(pf.test_tp_getattro(self.file, "encoding"), enc)
		self.assertEqual(pf.test_tp_getattro(self.file, "errors"), err)
		
	def test_file_getsetlist(self): # relies on PyFile_SetEncodingAndErrors, tp_getattro, tp_setattro and PyFile_SoftSpace working
		# Test closed
		self.assertFalse(pf.test_tp_getattro(self.file, "closed"))
		self.file.close()
		self.assertTrue(pf.test_tp_getattro(self.file, "closed"))
		# Test newlines (I don't really understand how to test this properly, but if it gives the same value as jython it's probably fine)
		self.assertEqual(self.file.newlines, pf.test_tp_getattro(self.file, "newlines"))
		# Test softspace
		pf.test_PyFile_SoftSpace(self.file, 1)
		self.assertEqual(1, pf.test_tp_getattro(self.file, "softspace"))
		s = 0
		pf.test_tp_setattro(self.file, "softspace", s)
		self.assertEqual(pf.test_tp_getattro(self.file, "softspace"), s)
	
	def test_tp_flags(self):
		self.assertEqual(pf.test_tp_flags(self.file), 134635, "The flags returned didn't equal the value 134635, I don't know what would break this, maybe which flags are on files has changed? or maybe the value of the flags is system dependent? I don't know.")
	
	def test_tp_doc(self):
		self.assertEqual(self.file.__doc__, pf.test_tp_doc(self.file))
		
	def test_tp_iter(self):
		#print pf.test_tp_iter(self.file)
		raise(Exception("Not yet Implemented"))
		
	def test_tp_iternext(self):
		#print pf.test_tp_iternext(self.file)
		raise(Exception("Not yet Implemented"))
	
	def test_file_readline(self):
		L1 = "Hello\n"
		self.file.write(L1)
		L2 = "World!"
		self.file.write(L2)
		self.file.close()
		self.file = open(self.name, "r+")
		self.assertEqual(pf.test_tp_getattro(self.file, "readline")(), L1)
		self.assertEqual(pf.test_tp_getattro(self.file, "readline")(), L2)
		
	def test_file_read(self):
		string = "Hello World!"
		self.file.write(string)
		self.file.close()
		self.file = open(self.name, "r+")
		self.assertEqual(pf.test_tp_getattro(self.file, "read")(), string)
	
	def test_file_write(self):
		string = "Hello World!"
		pf.test_tp_getattro(self.file, "write")(string)
		self.file.close()
		self.file = open(self.name, "r+")
		self.assertEqual(self.file.read(), string)
	
	def test_file_fileno(self):
		# TODO may need to change this to check it gives the file descriptor not org.python.core.io.FileIO@7523a3dc
		self.name = "/tmp/fred"
		self.mode = "+w"
		self.file = open(self.name, self.mode)
		self.assertEqual(pf.test_tp_getattro(self.file, "fileno")(), self.file.fileno())
	
	
	def test_file_seek(self):
		string = "Hello World!"
		self.file.write(string)
		pf.test_tp_getattro(self.file, "seek")(1)
		self.assertEqual(self.file.read(), string[1:])
	
	def test_file_truncate(self):
		string = "Hello World!"
		self.file.write(string)
		self.file.seek(7)
		pf.test_tp_getattro(self.file, "truncate")(8)
		self.assertEqual(self.file.read(), string[7])
		self.file.seek(3)
		pf.test_tp_getattro(self.file, "truncate")()
		self.file.seek(0)
		self.assertEqual(self.file.read(), string[:3])
		
	def test_file_tell(self):
		# This checks where we are in the file
		self.assertEqual(self.file.tell(), pf.test_tp_getattro(self.file, "tell")())
		self.file.write("Hello World!")
		self.file.seek(5)
		self.assertEqual(self.file.tell(), pf.test_tp_getattro(self.file, "tell")())
		
	def test_file_readinto(self):
		L1 = "Hello\n"
		self.file.write(L1)
		L2 = "World!"
		self.file.write(L2)
		self.file.close()
		self.file = open(self.name, "r+")
		# reads from file and puts into a buffer. test by creating two buffers and reading into from java and C then compare buffers
		testArr = bytearray('aaaaaaaaaaaa')
		testArr2 = bytearray('aaaaaaaaaaaa')
		self.file.readinto(testArr)
		self.file.seek(0)
		pf.test_tp_getattro(self.file, "readinto")(testArr2)
		self.assertEqual(testArr, testArr2)
		
	def test_file_readlines(self):
		L1 = "Hello\n"
		self.file.write(L1)
		L2 = "World!"
		self.file.write(L2)
		self.file.close()
		self.file = open(self.name, "r+")
		lines = pf.test_tp_getattro(self.file, "readlines")()
		self.file.close()
		self.file = open(self.name, "r+")
		self.assertEqual(lines, self.file.readlines())
		
	def test_file_xreadlines(self):
		L1 = "Hello\n"
		self.file.write(L1)
		L2 = "World!"
		self.file.write(L2)
		self.file.close()
		self.file = open(self.name, "r+")
		self.assertEqual(pf.test_tp_getattro(self.file, "xreadlines")(), self.file.xreadlines())
		self.file.close()
		# This is a terrible way to check they both generate the same output
		self.file = open(self.name, "r+")
		store = []
		for l in pf.test_tp_getattro(self.file, "xreadlines")():
			store.append(l)
		self.file.close()
		self.file = open(self.name, "r+")
		i = 0
		for l in self.file.xreadlines():
			self.assertEqual(store[i], l)
			i +=1
		
	def test_file_writelines(self):
		inpt = ["Hello\n", "World!"]
		pf.test_tp_getattro(self.file, "writelines")(inpt)
		self.file.seek(0)
		self.assertEqual(inpt, self.file.readlines());
		
	def test_file_flush(self):
		# try opening two files at the same time accessing the same place?
		s1 = "Hello "
		s2 = "World!"
		self.file.write(s1)
		self.file.close()
		self.file = open(self.name, "a")
		self.file.write(s2)
		self.file2 = open(self.name, "r")
		self.assertEqual(self.file2.read(), s1)
		pf.test_tp_getattro(self.file, "flush")()
		self.file2.close()
		self.file2 = open(self.name, "r")
		self.assertEqual(self.file2.read(), s1+s2)
		
	def test_file_close(self):
		self.assertFalse(self.file.closed, "self.file.closed isn't working properly so this test won't work!")
		pf.test_tp_getattro(self.file, "close")()
		self.assertTrue(self.file.closed, "file_close hasn't worked properly")
	
	def test_file_isatty(self): 
		# Not sure what this is, but this checks it gets the right value on at least one occasion,
		# this tells us that it is probably calling java correctly
		# if the call is to the correct method and it works once then it should always work
		self.assertEqual(self.file.isatty(), pf.test_tp_getattro(self.file, "isatty")())


	# Possibly test together, enter and check file is valid, exit and check file is closed and done etc
	def test_file___enter__ANDfile___exit__(self):
		temp = pf.test_tp_getattro(self.file, "__enter__")()
		self.assertEqual(type(temp), type(self.file))
		self.assertEqual(temp.name, self.file.name)
		self.assertEqual(temp.mode, self.file.mode)
		temp.write("Hello World!")
		pf.test_tp_getattro(temp, "__exit__")(temp, None, None)
		self.assertTrue(temp.closed)


	def test_tp_init(self):
		# TODO this may be the wrong way to pass the arguments in
		newName, newMode = "Hello", "r+"
		pf.test_tp_init(self.file, [newName, newMode, -1], ["name", "mode", "buffering"])
		# This should be a valid test although the code isn't passing yet
		self.assertEqual(self.file.name, newName)
		self.assertEqual(self.file.mode, newMode)
	
	def test_tp_alloc(self):
		raise(Exception("Not yet Implemented"))
	
	def test_tp_new(self):
		f = pf.test_tp_new(self.file)
		self.assertEqual(type(f), type(self.file))
		
	def test_tp_free(self):
		raise(Exception("Not yet Implemented"))



if __name__ == '__main__':
	# Failing:
	#print "start"
	#suite = unittest.TestLoader().loadTestsFromName("test_tp_init", TestPyFile)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_tp_iter", TestPyFile)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_tp_iternext", TestPyFile)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	#suite = unittest.TestLoader().loadTestsFromName("test_PyObject_AsFileDescriptor", TestPyFile)
	#unittest.TextTestRunner(verbosity=2).run(suite)
	# TODO: tp_free, tp_alloc, tp_dealloc, tp_weaklistoffset
	unittest.main()