```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/ros2-rust/rosidl_rust/noble-jazzy/ ./" | sudo tee /etc/apt/sources.list.d/ros2-rust_rosidl_rust-noble-jazzy.list
echo "yaml https://github.com/ros2-rust/rosidl_rust/raw/noble-jazzy/local.yaml jazzy" | sudo tee /etc/ros/rosdep/sources.list.d/1-ros2-rust_rosidl_rust-noble-jazzy.list
```
