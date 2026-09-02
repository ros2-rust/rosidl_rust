```bash
echo "deb [trusted=yes] https://raw.githubusercontent.com/ros2-rust/rosidl_rust/noble-kilted/ ./" | sudo tee /etc/apt/sources.list.d/ros2-rust_rosidl_rust-noble-kilted.list
echo "yaml https://github.com/ros2-rust/rosidl_rust/raw/noble-kilted/local.yaml kilted" | sudo tee /etc/ros/rosdep/sources.list.d/1-ros2-rust_rosidl_rust-noble-kilted.list
```
