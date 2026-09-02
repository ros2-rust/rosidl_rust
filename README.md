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

## AI Policy
Generative tools are allowed in producing contributions to its projects, with some qualifications:

- Any contribution may consist, in whole or in part, of the output of one or more generative tools.
- Any use of generative tools in a contribution must be disclosed at the time of making the contribution.
- The disclosure must be recorded in a way that ensures it has the same or greater lifetime as the contribution itself.

For source code contributions, you should add a disclosure statement in the commit message for all commits where some portion of the source code was generated.

`Assisted-by: AGENT_NAME:MODEL_VERSION [TOOL1] [TOOL2]`

Provide a similar disclosure statement in the PR description.

See the projects [AI Policy](https://github.com/ros2-rust/ros2_rust/blob/main/docs/AI_POLICY.md) for more details.
