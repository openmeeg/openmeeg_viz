import sys
from os import path as op
import openmeeg as om
import numpy as np
from openmeeg_viz import display_vtp # visualiation with VTK
from openmeeg_viz import display_vtk # visualiation with VTK


base_dir = op.join(op.dirname(__file__), 'data')

m = om.Mesh(op.join(base_dir,'brain.tri'))
m.save_vtk(op.join(base_dir,'brain.vtk'))

geo = om.Geometry(op.join(base_dir,'sample.geom'))
mat = om.Matrix(geo.size(),2)
potentials = np.random.random_sample((geo.size(),2)) #random potentials/current
mat = om.fromarray(potentials)
geo.write_vtp(op.join(base_dir,'sample.vtp'), mat)

def test_display_vtp():
    assert(display_vtp(op.join(base_dir,"sample.vtp")) == None)

def test_display_vtk():
    potentials = np.random.random_sample((m.nb_vertices(),1))
    assert(display_vtk(op.join(base_dir,"brain.vtk"), potentials) == None)
