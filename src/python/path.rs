use crate::path;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyfunction]
pub fn get_path_seperator() -> char {
    path::get_path_seperator()
}

#[pyclass]
pub struct PathUpdater {
    inner: path::PathUpdater,
}

#[pymethods]
impl PathUpdater {
    #[new]
    pub fn new(path_seperator: char) -> Self {
        Self {
            inner: path::PathUpdater::new(path_seperator),
        }
    }

    pub fn update_paths(
        &self,
        path_var_name: &str,
        new_path: Vec<String>,
        old_path: Vec<String>,
    ) -> PyResult<String> {
        Ok(self.inner.update_paths(
            &path_var_name,
            &new_path.iter().map(|s| s.as_str()).collect(),
            &old_path.iter().map(|s| s.as_str()).collect(),
        ))
    }
}
