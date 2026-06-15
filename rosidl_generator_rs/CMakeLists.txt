cmake_minimum_required(VERSION 3.12)

project(rosidl_generator_rs)

find_package(ament_cmake REQUIRED)

if("$ENV{ROS_DISTRO}" STRLESS_EQUAL "humble")
  find_package(rosidl_cmake REQUIRED)
  ament_export_dependencies(rosidl_cmake)
endif()

ament_export_dependencies(ament_cmake)
ament_export_dependencies(rmw)

ament_index_register_resource("rosidl_generator_packages")

ament_python_install_package(${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # The Python sources are checked by Ruff in CI. Copyright and docstring
  # linters are noisy for template files in this generator package.
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_flake8_FOUND TRUE)
  set(ament_cmake_pep257_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package(
  CONFIG_EXTRAS
    "rosidl_generator_rs-extras.cmake.in"
    "cmake/register_rs.cmake"
)

install(
  DIRECTORY cmake
  DESTINATION share/${PROJECT_NAME}
)
ament_register_extension(
  "rosidl_generate_idl_interfaces"
  "rosidl_generator_rs"
  "${PROJECT_SOURCE_DIR}/cmake/rosidl_generator_rs_generate_interfaces.cmake")

install(
  PROGRAMS bin/rosidl_generator_rs
  DESTINATION lib/rosidl_generator_rs
)
install(
  DIRECTORY cmake resource
  DESTINATION share/${PROJECT_NAME}
)
