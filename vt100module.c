#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "libvt100/src/vt100.h"

static PyObject *py_vt100_new(PyObject *self, PyObject *args)
{
    VT100Screen *vt;
    int rows, cols;

    if (!PyArg_ParseTuple(args, "ii", &rows, &cols)) {
        return NULL;
    }

    vt = vt100_screen_new(rows, cols);

    return Py_BuildValue("n", (Py_ssize_t)vt);
}

static PyObject *py_vt100_set_window_size(PyObject *self, PyObject *args)
{
    VT100Screen *vt;
    int rows, cols;

    if (!PyArg_ParseTuple(args, "nii", &vt, &rows, &cols)) {
        return NULL;
    }

    vt100_screen_set_window_size(vt, rows, cols);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *py_vt100_process_string(PyObject *self, PyObject *args)
{
    VT100Screen *vt;
    char *str;
    size_t len;
    int processed;

    if (!PyArg_ParseTuple(args, "ns#", &vt, &str, &len)) {
        return NULL;
    }

    processed = vt100_screen_process_string(vt, str, len);

    return PyLong_FromLong(processed);
}

static PyObject *py_vt100_cell_at(PyObject *self, PyObject *args)
{
    VT100Screen *vt;
    int row, col;
    struct vt100_cell *cell;

    if (!PyArg_ParseTuple(args, "nii", &vt, &row, &col)) {
        return NULL;
    }

    cell = vt100_screen_cell_at(vt, row, col);

    return Py_BuildValue("n", (Py_ssize_t)cell);
}

static PyObject *py_vt100_get_string_formatted(PyObject *self, PyObject *args)
{
    VT100Screen *vt;
    struct vt100_loc start, end;
    char *outstr;
    size_t outlen;

    if (!PyArg_ParseTuple(args, "niiii", &vt, &start.row, &start.col, &end.row, &end.col)) {
        return NULL;
    }

    vt100_screen_get_string_formatted(vt, &start, &end, &outstr, &outlen);

#if PY_MAJOR_VERSION == 3
    return Py_BuildValue("y#", outstr, outlen);
#else
    return Py_BuildValue("s#", outstr, outlen);
#endif
}

static PyObject *py_vt100_get_string_plaintext(PyObject *self, PyObject *args)
{
    VT100Screen *vt;
    struct vt100_loc start, end;
    char *outstr;
    size_t outlen;

    if (!PyArg_ParseTuple(args, "niiii", &vt, &start.row, &start.col, &end.row, &end.col)) {
        return NULL;
    }

    vt100_screen_get_string_plaintext(vt, &start, &end, &outstr, &outlen);

#if PY_MAJOR_VERSION == 3
    return Py_BuildValue("y#", outstr, outlen);
#else
    return Py_BuildValue("s#", outstr, outlen);
#endif
}

static PyObject *py_vt100_delete(PyObject *self, PyObject *args)
{
    VT100Screen *vt;

    if (!PyArg_ParseTuple(args, "n", &vt)) {
        return NULL;
    }

    vt100_screen_delete(vt);

    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef vt100_methods[] = {
    { "new", py_vt100_new, METH_VARARGS, "create a new vt100 object" },
    { "set_window_size", py_vt100_set_window_size, METH_VARARGS, "create a new vt100 object" },
    { "process_string", py_vt100_process_string, METH_VARARGS, "create a new vt100 object" },
    { "cell_at", py_vt100_cell_at, METH_VARARGS, "create a new vt100 object" },
    { "get_string_formatted", py_vt100_get_string_formatted, METH_VARARGS, "create a new vt100 object" },
    { "get_string_plaintext", py_vt100_get_string_plaintext, METH_VARARGS, "create a new vt100 object" },
    { "delete", py_vt100_delete, METH_VARARGS, "create a new vt100 object" },
    { NULL, NULL, 0, NULL }
};

#if PY_MAJOR_VERSION == 3
static struct PyModuleDef vt100module = {
    PyModuleDef_HEAD_INIT,
    "vt100_raw",
    NULL,
    -1,
    vt100_methods
};

PyMODINIT_FUNC PyInit_vt100_raw()
{
    return PyModule_Create(&vt100module);
}
#else
PyMODINIT_FUNC initvt100_raw()
{
    (void) Py_InitModule("vt100_raw", vt100_methods);
}
#endif
