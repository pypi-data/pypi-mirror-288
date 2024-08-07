import glob
import os

def cppimport_cfg( cfg ):
    base = os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) ) ) ) )
    pd = os.path.join( base, 'modules', 'PowerDiagram', 'src', 'cpp' )
    pc = os.path.join( base, 'src', 'cpp' )

    #     glob.glob( pd + '/PowerDiagram/support/display/*.cpp' )
    #     glob.glob( pd + '/PowerDiagram/support/string/read_arg_name.cpp' )
    sources = [ pd + '/PowerDiagram/VtkOutput.cpp' ]
              
    deps = [ 'polycon_bindings.h' ] + \
            glob.glob( pc + '/polycon/*.tcc' ) + \
            glob.glob( pc + '/polycon/*.h' ) + \
            glob.glob( pd + '/PowerDiagram/*.tcc' ) + \
            glob.glob( pd + '/PowerDiagram/*.h' )
        
    if os.name == 'nt':
        cfg['extra_compile_args'] = ['/std:c++20','-DAVOID_DISPLAY=1']
    else:
        cfg['extra_compile_args'] = ['-std=c++20','-DAVOID_DISPLAY=1']

    if "CONDA_PREFIX" in os.environ:
        cfg['extra_compile_args'].append( '-I' + os.environ[ "CONDA_PREFIX" ] + "/include" )

    cfg['include_dirs'] = [ pc, pd ]
    cfg['dependencies'] = deps
    cfg['sources'] = sources
