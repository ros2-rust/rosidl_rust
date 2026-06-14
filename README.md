# rosidl_rust

rosidl support for Rust

## Debian packages

The Debian package build workflow publishes apt repositories to package branches
named `<ubuntu-codename>-<ros-distro>`.

| ROS distribution | Ubuntu distribution | Package branch |
| --- | --- | --- |
| Rolling | Resolute | `resolute-rolling` |
| Lyrical | Resolute | `resolute-lyrical` |
| Kilted | Noble | `noble-kilted` |
| Jazzy | Noble | `noble-jazzy` |
| Humble | Jammy | `jammy-humble` |

To install the generated packages, choose the matching package branch for your
ROS and Ubuntu distribution:

```bash
export ROS_DISTRO=rolling
export PACKAGE_BRANCH=resolute-rolling

echo "deb [trusted=yes] https://raw.githubusercontent.com/ros2-rust/rosidl_rust/${PACKAGE_BRANCH}/ ./" \
  | sudo tee "/etc/apt/sources.list.d/ros2-rust-rosidl-rust-${PACKAGE_BRANCH}.list"

echo "yaml https://raw.githubusercontent.com/ros2-rust/rosidl_rust/${PACKAGE_BRANCH}/local.yaml ${ROS_DISTRO}" \
  | sudo tee "/etc/ros/rosdep/sources.list.d/1-ros2-rust-rosidl-rust-${PACKAGE_BRANCH}.list"

sudo apt update
rosdep update
sudo apt install "ros-${ROS_DISTRO}-rosidl-generator-rs"
```

Replace `ROS_DISTRO` and `PACKAGE_BRANCH` with the matching values from the
table above.

Generated package versions use the nearest reachable tag, the number of commits
since that tag, the commit date in UTC, and the short commit SHA. For example,
a package built from tag `0.4.13` sorts below the official ROS buildfarm release:

```text
0.4.13-0~2026.06.14.22.00+gabcdef123456
```

A package built from a newer commit after that tag sorts above the older tagged
release while remaining deterministic for rebuilds of the same commit:

```text
0.4.13+git1-0~2026.06.15.09.30+g123456abcdef
```
