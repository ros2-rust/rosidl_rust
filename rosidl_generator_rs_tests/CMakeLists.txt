cmake_minimum_required(VERSION 3.12)

project(rosidl_generator_rs_tests)

find_package(ament_cmake REQUIRED)
find_package(action_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rosidl_generator_rs REQUIRED)
find_package(unique_identifier_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Complex.msg"
  "msg/Keywords.msg"
  "srv/Compute.srv"
  "action/DoThing.action"
  DEPENDENCIES action_msgs builtin_interfaces unique_identifier_msgs
)

ament_package()
