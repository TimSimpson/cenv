use crate::path;
use pyo3::prelude::*;

#[pyfunction]
pub fn get_path_seperator() -> char {
    path::get_path_seperator()
}
