use std::error::Error;
use reqwest;

pub fn fetch_html(url: &str) -> Result<String, Box<dyn Error>> {
    let body = reqwest::blocking::get(url)?.text()?;
    Ok(body)
}
