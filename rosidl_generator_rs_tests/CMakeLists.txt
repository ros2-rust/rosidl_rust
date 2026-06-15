cmake_minimum_required(VERSION 3.12)

project(rosidl_generator_rs_tests)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rosidl_generator_rs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Complex.msg"
  "msg/Keywords.msg"
  "srv/Compute.srv"
  "action/DoThing.action"
)

ament_package()
