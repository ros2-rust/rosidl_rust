#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};

@{
TEMPLATE(
    'templates/msg_idiomatic.rs.em',
    package_name=package_name, interface_path=interface_path,
    representation=representation,
    get_public_rs_type=get_public_rs_type,
    public_conversion=public_conversion,
    msg_specs=msg_specs,
    get_rs_name=get_rs_name,
    get_rs_type=make_get_rs_type(True),
    pre_field_serde=pre_field_serde,
    constant_value_to_rs=constant_value_to_rs)
}@

@[if representation == 'cpu' and buffer_enabled]@
rosidl_runtime_rs::cfg_buffer! {
/// Backend-neutral buffer representation of the same ROS interfaces.
#[cfg(feature = "rosidl-buffer")]
pub mod buffer {
    #[allow(unused_imports)]
    use super::*;
    include!("@(namespace)/buffer.rs");
}
}
@[end if]@
