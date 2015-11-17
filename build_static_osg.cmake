MESSAGE("+++ Building local osg")
SET(OSG_INSTALL_DIR ${CMAKE_BINARY_DIR}/_osg_static)
FILE(MAKE_DIRECTORY ${OSG_INSTALL_DIR})

SET(OSG_SRC_DIR ${CMAKE_SOURCE_DIR}/dependencies/OpenSceneGraph-3.2.0/)

# A target which depends on STATIC_OSG_LIBRARY
ADD_CUSTOM_COMMAND(OUTPUT __static_osg_was_run__
    COMMAND ${CMAKE_COMMAND} 
        -DCMAKE_INSTALL_PREFIX=${OSG_INSTALL_DIR}
        -DBUILD_OSG_APPLICATIONS:BOOL=OFF
        -DDYNAMIC_OPENSCENEGRAPH:BOOL=OFF
        ${OSG_SRC_DIR}
    COMMAND $(MAKE)
    COMMAND $(MAKE) install
    WORKING_DIRECTORY ${OSG_INSTALL_DIR}
    VERBATIM
    )

ADD_CUSTOM_TARGET(_libosg ALL 
    DEPENDS __static_osg_was_run__
    )

LIST(APPEND ALL_STATIC_LIBS ${STATIC_OSG_LIBRARY})
add_dependencies(_moose_static_dependencies _libosg)
