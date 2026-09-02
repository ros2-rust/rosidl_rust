```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/ros2-rust/rosidl_rust/jammy-humble/ ./" | sudo tee /etc/apt/sources.list.d/ros2-rust_rosidl_rust-jammy-humble.list
echo "yaml https://github.com/ros2-rust/rosidl_rust/raw/jammy-humble/local.yaml humble" | sudo tee /etc/ros/rosdep/sources.list.d/1-ros2-rust_rosidl_rust-jammy-humble.list
```
