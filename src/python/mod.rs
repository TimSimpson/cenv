use pyo3::prelude::*;

mod options;
mod path;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a - b).to_string())
}

/// A Python module implemented in Rust.
// #[pymodule]
// fn cenv(m: &Bound<'_, PyModule>) -> PyResult<()> {
//     m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
//     Ok(())
// }

#[pymodule]
fn _cenv(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(path::get_path_seperator, m)?)?;
    m.add_class::<options::Options>()?;
    Ok(())
}
