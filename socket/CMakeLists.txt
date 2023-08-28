cmake_minimum_required(VERSION 3.13)
project(test_cmake CXX)

# add_subdirectory(src)
add_subdirectory(test)

enable_testing()
add_test(NAME test COMMAND test/a.out)