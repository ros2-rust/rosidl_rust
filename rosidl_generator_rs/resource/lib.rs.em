#![allow(non_camel_case_types)]
#![allow(clippy::derive_partial_eq_without_eq)]
#![allow(clippy::upper_case_acronyms)]

@[if len(msg_specs) > 0]@
#[path = "msg.rs"]
mod msg_idiomatic;
pub mod msg {
    pub use super::msg_idiomatic::*;
    pub mod rmw;
}
@[end if]@

@[if len(srv_specs) > 0]@
#[path = "srv.rs"]
mod srv_idiomatic;
pub mod srv {
    pub use super::srv_idiomatic::*;
    pub mod rmw;
}
@[end if]@

@[if len(action_specs) > 0]@
#[path = "action.rs"]
mod action_idiomatic;
pub mod action {
    pub use super::action_idiomatic::*;
    pub mod rmw;
}
@[end if]@
