
m=om.Mesh('data/brain.tri')
m.save_vtk('data/brain.vtk')

geo=om.Geometry('data/sample.geom')
geo.write_vtp('data/sample.vtp')

def test_om_display_vtp(self):
    assert(om_display_vtp("data/sample.vtp"))

def test_om_display_vtp(self):
    assert(om_display_vtk("data/brain.vtk"))
