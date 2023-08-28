add_library(greetings SHARED hello.cpp good_morning.cpp)

find_package(OpenCV REQUIRED)
target_link_libraries(greetings ${OpenCV_LIBS})

target_include_directories(greetings PUBLIC  ${OpenCV_INCLUDE_DIRS} )
target_include_directories(greetings PUBLIC ${PROJECT_SOURCE_DIR}/include)

target_compile_options(greetings PUBLIC -O2 -Wall)
target_compile_features(greetings PUBLIC cxx_std_17)
