```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/ros2-rust/rosidl_rust/resolute-rolling/ ./" | sudo tee /etc/apt/sources.list.d/ros2-rust_rosidl_rust-resolute-rolling.list
echo "yaml https://github.com/ros2-rust/rosidl_rust/raw/resolute-rolling/local.yaml rolling" | sudo tee /etc/ros/rosdep/sources.list.d/1-ros2-rust_rosidl_rust-resolute-rolling.list
```
