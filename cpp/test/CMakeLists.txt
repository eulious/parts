add_executable(a.out main.cpp)

# find_package(OpenCV REQUIRED)
# include_directories( ${OpenCV_INCLUDE_DIRS} )

target_link_libraries(a.out greetings)
# target_link_libraries(a.out ${OpenCV_LIBS})
target_compile_options(a.out PUBLIC -O2 -Wall)
target_compile_features(a.out PUBLIC cxx_std_17)