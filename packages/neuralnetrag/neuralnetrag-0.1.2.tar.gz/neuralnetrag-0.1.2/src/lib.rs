use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod fetch;
mod parse;
mod similarity;

use fetch::fetch_html;
use parse::parse_html;
use similarity::retrieve_similarity;

#[pyfunction]
pub fn retrieve(url: &str, query: &str, k: usize, chunk_size: usize) -> PyResult<Vec<String>> {
    match fetch_html(url) {
        Ok(content) => {
            let chunks = parse_html(&content, chunk_size);
            let mut scored_chunks: Vec<(String, f64)> = chunks.into_iter()
                .map(|chunk| (chunk.clone(), retrieve_similarity(query, &chunk)))
                .collect();

            scored_chunks.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));

            let top_k_chunks = scored_chunks.into_iter()
                .take(k)
                .map(|(chunk, _)| chunk)
                .collect();

            Ok(top_k_chunks)
        }
        Err(e) => Err(pyo3::exceptions::PyRuntimeError::new_err(e.to_string())),
    }
}

#[pymodule]
fn neuralnetrag(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(retrieve, m)?)?;
    Ok(())
}
