cmake_minimum_required(VERSION 3.1)
project(test_package LANGUAGES C CXX)

find_package(woff2 REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} woff2::woff2)
