[package]
name = "@(package_name)"
version = "@(package_version)"
edition = "2021"

[dependencies]
@[if buffer_enabled]@
rosidl_runtime_rs = { version = "0.7", features = ["rosidl-buffer"] }
rosidl_buffer_rs = "0.1"
@[else]@
rosidl_runtime_rs = "0.7"
@[end if]@
serde = { version = "1", optional = true, features = ["derive"] }
serde-big-array = { version = "0.5.1", optional = true }

# ROS Dependencies
@[for dep in dependency_packages]@
@(dep) = "*"
@[end for]@

[features]
@[if buffer_enabled]@
default = ["rosidl-buffer"]
rosidl-buffer = []
@[end if]@
@{
serde_features = ["dep:serde", "dep:serde-big-array", "rosidl_runtime_rs/serde"]
if buffer_enabled:
    serde_features.append("rosidl_buffer_rs/serde")
for dep in dependency_packages:
	serde_features.append("{}/serde".format(dep))
}@
serde = @(serde_features)

[package.metadata.ros-env]
include = true
