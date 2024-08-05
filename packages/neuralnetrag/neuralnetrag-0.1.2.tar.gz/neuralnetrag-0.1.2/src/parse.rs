use select::document::Document;
use select::predicate::Name;

pub fn parse_html(html: &str, chunk_size: usize) -> Vec<String> {
    let document = Document::from(html);
    let mut chunks = Vec::new();
    let mut current_chunk = String::new();

    // Iterate over all paragraphs (<p>) in the HTML
    for node in document.find(Name("p")) {
        let text = node.text();
        
        // Check if adding this text exceeds the chunk size
        if current_chunk.len() + text.len() > chunk_size {
            chunks.push(current_chunk);
            current_chunk = String::new();
        }
        
        // Add the text to the current chunk
        current_chunk.push_str(&text);
        current_chunk.push(' '); // Add a space to separate paragraphs
    }
    
    // Add any remaining text as a final chunk
    if !current_chunk.is_empty() {
        chunks.push(current_chunk);
    }

    chunks
}
