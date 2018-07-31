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
 * DemoExtensionmodule.c
 *
 *  Created on: 2018-07-30 13:35
 *	  Author: Calum Freeman
 */

#include <Python.h>

#ifndef MS_WINDOWS
#define _alloca alloca
#endif
PyMODINIT_FUNC initPyFileTest(void);
// make some macros to expand the stuff needed for python to understand this module
// Basically MakeTest(functionName) then in pyMethodDef MapTest(functionName) and that will expose test_functionName to python
#define MakeTest(X) static PyObject* testPyFile_ ## X (PyObject *self, PyObject *args);\
static char X ## _docs[] = "This tests the "#X" function"
#define MapTest(X) { "test_"#X, (PyCFunction)testPyFile_ ## X, METH_VARARGS, X ## _docs }

// declare functions, doc strings and method def's
MakeTest(PyFile_WriteString);
MakeTest(PyFile_AsFile);
MakeTest(PyFile_Name);
MakeTest(file_repr);
MakeTest(PyFile_FromFile);

// declare doc strings
static char PyFile_docs[]= "this tests the PyFile API";

// declare module map
static PyMethodDef PyFileTestMethods[] = {
		MapTest(PyFile_WriteString),
		MapTest(PyFile_AsFile),
		MapTest(PyFile_Name),
		MapTest(file_repr),
		MapTest(PyFile_FromFile),
		{ NULL, NULL, 0, NULL }
};



// define functions
static PyObject* testPyFile_PyFile_WriteString(PyObject *self, PyObject *args) {
	PyObject *f;
	char *myStr;
	if (!PyArg_ParseTuple(args, "Os", &f, &myStr)) {
		printf("PyArg_ParseTuple in testPyFile_PyFile_WriteString didn't work\n");
		return Py_BuildValue("i", -1);
	}

	// TODO check that the file actually wrote successfully check with empty and non-empty files
	int successReturn = PyFile_WriteString(myStr, f);
	if(successReturn!=0) return Py_BuildValue("i", -1);

	int errorReturn = PyFile_WriteString(myStr, NULL);
	if(errorReturn!=-1) return Py_BuildValue("i", -1);

	// TODO find a way to throw a java IO exception that can be caught by JNI and trigger this block
	//int javaErrorReturn = PyFile_WriteString(myStr, NULL);
	//if(javaErrorReturn!=-2) return NULL;

	//free(myStr);
	return Py_BuildValue("i", 1);
}

static PyObject* testPyFile_PyFile_AsFile(PyObject *self, PyObject *args){
	// takes in a file containing a character and that character then gets a file pointer and uses it to see if the char is there, if it is then this is probably pointing to the right file
	PyObject *Obj;
	char myCh;
	if (!PyArg_ParseTuple(args, "Oc", &Obj, &myCh)) {
		printf("PyArg_ParseTuple in testPyFile_PyFile_AsFile didn't work\n");
	    return NULL;
	}
	FILE *f = PyFile_AsFile(Obj);
	if(f == NULL){
		return Py_BuildValue("s", "file is closed");
	}
	char ch = fgetc(f);
	return Py_BuildValue("c", ch);
}

static PyObject* testPyFile_PyFile_Name(PyObject *self, PyObject *args){
	PyObject *Obj;
	PyObject *name;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	PyFileObject *Test = (PyFileObject *)Obj;
	return PyFile_Name(Obj);
}

static PyObject* testPyFile_file_repr(PyObject *self, PyObject *args){
	PyObject *Obj;
	if (!PyArg_ParseTuple(args, "O", &Obj)) {
		printf("PyArg_ParseTuple in testPyFile_file_repr didn't work\n");
		return NULL;
	}
	PyObject* pstr = Obj->ob_type->tp_repr(Obj);
	char* str = PyString_AsString(pstr);
	return Py_BuildValue("s", str);
}

static PyObject* testPyFile_PyFile_FromFile(PyObject *self, PyObject *args){
	PyObject *Obj;
	char* Cname;
	char* Cmode;
	if (!PyArg_ParseTuple(args, "Oss", &Obj, &Cname, &Cmode)) {
		printf("PyArg_ParseTuple in testPyFile_PyObject_AsFileDescriptor didn't work\n");
		return NULL;
	}
	FILE* file = PyFile_AsFile(Obj);
	PyObject *o = PyFile_FromFile(file, Cname, Cmode, (int (*)(FILE *))NULL);
	// TODO check the PyFile works/is what we expect
	return Py_BuildValue("O", o);
}

//initialise module
PyMODINIT_FUNC
initPyFileTest(void)
{
	(void)Py_InitModule3("PyFileTest", PyFileTestMethods, PyFile_docs);
}
