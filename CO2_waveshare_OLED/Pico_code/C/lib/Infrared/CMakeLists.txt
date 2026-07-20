# Search for all source files in the current directory
# and save the names to the DIR_Infrared_SRCS variable
aux_source_directory(. DIR_Infrared_SRCS)

include_directories(../Config)

# Generate link library
add_library(Infrared ${DIR_Infrared_SRCS})
target_link_libraries(Infrared PUBLIC Config)