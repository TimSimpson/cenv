use crate::options;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
pub struct Options {
    inner: options::Options,
}

#[pymethods]
impl Options {
    #[new]
    pub fn new(root_directory: &str) -> PyResult<Self> {
        match options::Options::new(root_directory) {
            Ok(inner) => Ok(Self { inner }),
            Err(err) => Err(PyValueError::new_err(err.to_string())),
        }
    }

    pub fn _from_root(&self, path: &str) -> PyResult<String> {
        Ok(self.inner.get_from_root(path).to_string_lossy().to_string())
    }

    #[getter]
    pub fn batch_file(&self) -> PyResult<String> {
        Ok(self.inner.batch_file().to_string_lossy().to_string())
    }

    #[getter]
    pub fn environments(&self) -> PyResult<String> {
        Ok(self.inner.environments().to_string_lossy().to_string())
    }

    #[getter]
    pub fn rc_file(&self) -> PyResult<String> {
        Ok(self.inner.rc_file().to_string_lossy().to_string())
    }

    #[getter]
    pub fn root_directory(&self) -> PyResult<String> {
        Ok(self.inner.root_directory().to_string_lossy().to_string())
    }
}
