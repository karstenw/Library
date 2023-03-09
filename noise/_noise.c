// PERLIN NOISE
// C version of Ken Perlin's improved noise.
// Based on Malcolm Kesson's code: http://www.fundza.com/c4serious/noise/perlin/perlin.html
// © 2002-4 Malcolm Kesson. All rights reserved.
/* -------------------------------------------------------------------------------------- */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static int p[512];
void init_p_array(int i)
{
    // Populate the permutation array p (defines the pattern of the noise).
    srand((unsigned)i);
    for(i=0; i<256; i++)     
        p[i] = p[256+i] = rand()%256;
}

double fade(double t) { return t * t * t * (t * (t * 6 - 15) + 10); }
double lerp(double t, double a, double b) { return a + t * (b - a); }
double grad(int hash, double x, double y, double z) 
{
    // Convert lo 4 bits of hash code into 12 gradient directions.
    int     h = hash & 15;
    double  u = h < 8 ? x : y,
            v = h < 4 ? y : h==12 || h==14 ? x : z;
    return ((h&1) == 0 ? u : -u) + ((h&2) == 0 ? v : -v);
}

double noise(double x, double y, double z)
{
    // Find unit cuve that contains point.
    int   X = (int)floor(x) & 255,
          Y = (int)floor(y) & 255,
          Z = (int)floor(z) & 255;

    // Find relative x, y, z of point in cube.
    x -= floor(x);
    y -= floor(y);
    z -= floor(z);
    
    // Compute fade curves for each of x, y, z.
    double  u = fade(x),
            v = fade(y),
            w = fade(z);
            
    // Hash coordinates of the 8 cube corners.
    int  A  = p[X  ] + Y,
         AA = p[A  ] + Z,
         AB = p[A+1] + Z,
         B  = p[X+1] + Y,
         BA = p[B  ] + Z,
         BB = p[B+1] + Z;

    // Add blended results from 8 corners of cube.
    return lerp(w, 
        lerp(v, 
            lerp(u, grad(p[AA  ], x  , y  , z  ), 
                    grad(p[BA  ], x-1, y  , z  )),
            lerp(u, grad(p[AB  ], x  , y-1, z  ), 
                    grad(p[BB  ], x-1, y-1, z  ))),
        lerp(v, 
            lerp(u, grad(p[AA+1], x  , y  , z-1), 
                    grad(p[BA+1], x-1, y  , z-1)),
            lerp(u, grad(p[AB+1], x  , y-1, z-1), 
                    grad(p[BB+1], x-1, y-1, z-1)))
        );
}


/* Python bindings */
/* -------------------------------------------------------------------------------------- */

#define PY_SSIZE_T_CLEAN
#include <Python.h> 

#if PY_MAJOR_VERSION >= 3
  #define MOD_ERROR_VAL NULL
  #define MOD_SUCCESS_VAL(val) val
  #define MOD_INIT(name) PyMODINIT_FUNC PyInit_##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
          static struct PyModuleDef moduledef = { \
            PyModuleDef_HEAD_INIT, name, doc, -1, methods, }; \
          ob = PyModule_Create(&moduledef);
#else
  #define MOD_ERROR_VAL
  #define MOD_SUCCESS_VAL(val)
  #define MOD_INIT(name) void init##name(void)
  #define MOD_DEF(ob, name, doc, methods) \
    ob = Py_InitModule3(name, methods, doc);
#endif


// A typical Python binding:
// get parameters from tuple and pass them to the C function.
static PyObject *
perlin(PyObject *self, PyObject *args) {
    // Calls noise() with x, y, z parameters and returns d.
    double x, y, z, d;   
    if (!PyArg_ParseTuple(args, "ddd", &x, &y, &z)) return NULL;
    d = noise(x, y, z);
    return Py_BuildValue("d", d);
}

static PyObject *
seed(PyObject *self, PyObject *args) {
    // Calls init() to populate p with random numbers based on given seed.
    int i;   
    if (!PyArg_ParseTuple(args, "i", &i)) return NULL;
    init_p_array(i);
    return Py_BuildValue("");
}

static PyObject *
shape(PyObject *self, PyObject *args) {
    // Populates p from a Python list (must contain 512 integers < 512).
    PyObject *a;
    if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &a))
    	return NULL;

    int i;
    for(i=0; i<512; i++) {
        // p[i] = (int)PyInt_AsLong(PyList_GetItem(a, i));
        p[i] = (int)PyLong_FromLong(PyList_GetItem(a, i));
    }
    return Py_BuildValue("");
}

// List all Python bindings here.
static PyMethodDef noise_methods[]={ 
    { "perlin", perlin, METH_VARARGS },
    { "seed", seed, METH_VARARGS },
    { "shape", shape, METH_VARARGS },
    { NULL, NULL }
};

// Initialization goes here.
MOD_INIT(_noise) {
    PyObject *m;
    // m = Py_InitModule("_noise", noise_methods);
    MOD_DEF(m, "noise", "A C version of Ken Perlin's improved noise.", noise_methods )
    
    init_p_array(1);

#if PY_MAJOR_VERSION >= 3
    return(MOD_SUCCESS_VAL(m));
#else
	MOD_SUCCESS_VAL(m)
#endif

}

int main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_Initialize();
    //init_noise();
#if PY_MAJOR_VERSION >= 3
    PyInit__noise();
#else
    initnoise();
#endif
    return 0;
}
