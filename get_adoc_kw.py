#!/usr/local/bin/python3

import os
import re
import sys

def get_adoc_files( base_path ) :
    adoc_files = []
    for root, dir_names, file_names in os.walk( base_path ) :
        for file_name in file_names :
            if file_name.endswith( ".asciidoc" ) or file_name.endswith( ".adoc" ) :
                adoc_files.append( os.path.join( root, file_name ) )
    return adoc_files

'''assume only one keyword line exists in the document'''
def get_kw( file_name ) :
    context_expr = re.compile( r':keywords:(.+)' )
    with open( file_name, "r" ) as f :
        contents = f.readlines()
        for line in contents :
            match_attempt = context_expr.match( line )
            if match_attempt :
                kws = []
                for kw in match_attempt.group( 1 ).rstrip().split( "," ) :
                    kw = kw.rstrip().strip()
                    if kw != "" :
                        kws.append( kw )
                return kws

def get_all_kw( base_path ) :
    keywords = dict()
    adoc_files = get_adoc_files( base_path )
    for adoc_file in adoc_files :
        for kw in get_kw( adoc_file ) :
            if kw not in keywords :
                keywords[ kw ] = 1
            else :
                keywords[ kw ] = keywords[ kw ] + 1
    return keywords

def main( argv ) :
    if len( argv ) != 2 :
        sys.exit( -1 )
    else :
        print( get_all_kw( sys.argv[ 1 ] ) )

if __name__=="__main__" :
    main( sys.argv )
