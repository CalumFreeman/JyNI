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

class Test_PyFile(unittest.TestCase):
    
    def setUp(self):
        self.name = "/tmp/fred"
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
        self.assertFalse(True, "Not yet implemented")
    
    def test_PyFile_CheckExact(self):
        self.assertFalse(True, "Not yet implemented")
        
    def test_PyFile_IncUseCount(self):
        raise(Exception("Not yet Implemented"))
        
    def test_PyFile_DecUseCount(self):
        raise(Exception("Not yet Implemented"))
    
    @SkipTest
    def test_PyFile_WriteObject(self):
        raise(Exception("Not yet Implemented"))
      
    def test_tp_dealloc(self):
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
        print pf.test_tp_iter(self.file)
        self.assertTrue(False, "not done yet")
        
    def test_tp_iternext(self):
        print pf.test_tp_iternext(self.file)
        self.assertTrue(False, "not done yet")
    
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
        raise(Exception("Not yet Implemented"))
        
    def test_file_tell(self):
        self.assertFalse(True, "Not yet implemented")
        
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
        thing = pf.test_tp_getattro(self.file, "readinto")
        thing(testArr2)
        tmp = self.file.read()
        print testArr
        print testArr2
        self.assertFalse(True, "Not yet implemented")
        
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
        self.assertFalse(True, "Not yet implemented")
        
    def test_file_close(self):
        self.assertFalse(self.file.closed, "self.file.closed isn't working properly so this test won't work!")
        pf.test_tp_getattro(self.file, "close")()
        self.assertTrue(self.file.closed, "file_close hasn't worked properly")
        
    def test_file_isatty(self):
        self.assertEqual(self.file.isatty(), pf.test_tp_getattro(self.file, "isatty")())

        
    def test_file___enter__(self):
        self.assertFalse(True, "Not yet implemented")
        
    def test_file___exit__(self):
        self.assertFalse(True, "Not yet implemented")

    
    def test_tp_init(self):
        self.assertFalse(True, "Not yet implemented")
    
    def test_tp_alloc(self):
        self.assertFalse(True, "Not yet implemented")
        
    def test_tp_new(self):
        self.assertFalse(True, "Not yet implemented")
        
    def test_tp_free(self):
        self.assertFalse(True, "Not yet implemented")

    

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromName("test_file_isatty", Test_PyFile)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()