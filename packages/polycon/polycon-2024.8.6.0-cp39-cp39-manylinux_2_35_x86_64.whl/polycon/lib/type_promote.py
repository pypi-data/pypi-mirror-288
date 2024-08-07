import numpy as np

def type_name_of( value ):
    dtype = np.dtype( type( value ) )
    if dtype.kind == 'O':
        # try with Fraction
        try:
            from fractions import Fraction
            if isinstance( value, Fraction ):
                return "Rational"
        except:
            pass

        # well...
        print( type( value ) )
        raise NotImplemented
    return type_name_for_dtype( dtype )

def type_name_for_dtype( dtype ):
    """ item type => internal name, like FP64, Rational, ... """
    if not isinstance( dtype, np.dtype ):
        return type_name_for_dtype( np.dtype( dtype ) )

    kind = ""
    kind_map = { 'f': 'FP', 'i': 'SI' }
    if dtype.kind in kind_map:
        kind = kind_map[ dtype.kind ]
    else:
        print( dtype )
        raise NotImplemented

    size = dtype.itemsize * 8

    return kind + str( size )

def type_name_for_items_of( array_ ):
    array = np.asarray( array_ )
    if array.dtype.kind == 'O':
        return type_promote( [ type_name_of( v ) for v in array.flatten() ] )
    return type_name_for_dtype( array.dtype )

def type_promote( list : list[ str ], ensure_scalar = False ):
    kind = ''
    size = 4
    for type in list:
        ( type_kind, type_size ) = type_info( type )
        kind = best_kind( kind, type_kind )
        size = max( size, type_size )

    if ensure_scalar and kind in [ "SI", "PI" ]:
        return "Rational"
        
    return make_type( kind, size )

def type_info( type: str ):
    if type.startswith( 'FP' ) and len( type ) > 2 and all( t.isdigit() for t in type[ 2: ] ):
        return ( 'FP', int( type[ 2: ] ) )
    if type.startswith( 'SI' ) and len( type ) > 2 and all( t.isdigit() for t in type[ 2: ] ):
        return ( 'SI', int( type[ 2: ] ) )
    if type == 'Rational':
        return ( 'Rational', 1e6 )
    raise NotImplemented

def make_type( kind, size ):
    if kind in [ "Rational" ]:
        return kind
    return kind + str( size )

kind_value = { '': 0, 'PI': 1, 'SI': 2, 'FP': 3, 'Rational': 4 }
def best_kind( a, b ):
    if kind_value[ a ] >= kind_value[ b ]:
        return a
    else:
        return b

