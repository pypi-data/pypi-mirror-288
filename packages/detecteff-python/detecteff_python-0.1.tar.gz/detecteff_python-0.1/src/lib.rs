use pyo3::prelude::*;

mod detecteff;



#[pymodule]
#[pyo3(name = "rust")]
fn rust(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    let detecteff = PyModule::new_bound(py, "detecteff")?;
    detecteff.add_class::<detecteff::DetecteffRust>()?;
    // detecteff.add_function(wrap_pyfunction!(detecteff::print_help, detecteff)?)?;
    m.add_submodule(&detecteff)?;
    m.add_function(wrap_pyfunction!(detecteff::print_help, m)?)?;
    m.add_function(wrap_pyfunction!(detecteff::print_version, m)?)?;
    Ok(())
}