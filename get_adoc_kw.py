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

def get_keywords( context_expr, file_name ) :
    with open( file_name, "r" ) as f :
        file_contents = f.readlines()
        for line in file_contents :
            parsed_content = context_expr.match( line )
            if parsed_content :
                return [ x for x in map( lambda x: x.strip(), parsed_content.group( 1 ).rstrip().split( "," ) ) if x != "" ]
    return []

def get_all_keywords( base_path ) :
    keywords     = dict()
    context_expr = re.compile( r':keywords:(.+)' )
    adoc_files   = get_adoc_files( base_path )
    for adoc_file in adoc_files :
        for keyword in get_keywords( context_expr, adoc_file ) :
            if keyword not in keywords :
                keywords[ keyword ] = 1
            else :
                keywords[ keyword ] = keywords[ keyword ] + 1
    return keywords

def main( cmd_opts ) :
    if len( cmd_opts ) != 2 :
        sys.exit( -1 )
    else :
        print( get_all_keywords( sys.argv[ 1 ] ) )

if __name__=="__main__" :
    main( sys.argv )
