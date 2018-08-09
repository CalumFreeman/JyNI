/*
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
 *
 *
 *
 * IteratorsTestmodule.c
 *
 *  Created on: 2018-08-07 16:21
 *	  Author: Calum Freeman
 */

#include <Python.h>

#ifndef MS_WINDOWS
#define _alloca alloca
#endif
PyMODINIT_FUNC initIteratorsTest(void);
// make some macros to expand the stuff needed for python to understand this module
// Basically MakeTest(functionName) then in pyMethodDef MapTest(functionName) and that will expose test_functionName to python
#define MakeTest(X) static PyObject* test_ ## X (PyObject *self, PyObject *args);\
static char X ## _docs[] = "This tests the "#X" function"
#define MapTest(X) { "test_"#X, (PyCFunction)test_ ## X, METH_VARARGS, X ## _docs }

// SetBufSize SetEncoding SetEncodingAndErrors SoftSpace
// declare functions, doc strings and method def's
MakeTest(iternext);
// declare doc strings
static char Iterators_docs[]= "this tests the PyFile API";

// declare module map
static PyMethodDef IteratorsMethods[] = {
		MapTest(iternext),
		{ NULL, NULL, 0, NULL }

};


// define functions
static PyObject* test_iternext(PyObject *self, PyObject *args){
	PyObject *Obj;
	PyObject *thing;
	PyObject *iterator;
	int num;
	int i;
	if (!PyArg_ParseTuple(args, "Oi", &Obj, &num)) {
		printf("PyArg_ParseTuple in testPyFile_PyFile_Check didn't work\n");
		return NULL;
	}
	iterator = Obj->ob_type->tp_iter(Obj);
	for(i = 0;i<num;i++){
		thing = iterator->ob_type->tp_iternext(iterator);
	}
	return Py_BuildValue("O", thing);
}




//initialise module
PyMODINIT_FUNC
initIteratorsTest(void)
{
	(void)Py_InitModule3("IteratorsTest", IteratorsMethods, Iterators_docs);
}
