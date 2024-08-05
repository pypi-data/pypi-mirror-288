use std::collections::HashMap;

pub fn retrieve_similarity(query: &str, chunk: &str) -> f64 {
    let query_tokens = tokenize(query);
    let chunk_tokens = tokenize(chunk);

    let query_counter = count_words(&query_tokens);
    let chunk_counter = count_words(&chunk_tokens);

    let dot = dot_product(&query_counter, &chunk_counter);
    let magnitude_query = magnitude(&query_counter);
    let magnitude_chunk = magnitude(&chunk_counter);

    if magnitude_query > 0.0 && magnitude_chunk > 0.0 {
        (dot as f64) / (magnitude_query * magnitude_chunk)
    } else {
        0.0
    }
}

pub fn tokenize(text: &str) -> Vec<&str> {
    text.split_whitespace().collect()
}

pub fn count_words<'a>(tokens: &'a [&'a str]) -> HashMap<&'a str, usize> {
    let mut counter = HashMap::new();
    for &token in tokens {
        *counter.entry(token).or_insert(0) += 1;
    }
    counter
}

pub fn dot_product(counter1: &HashMap<&str, usize>, counter2: &HashMap<&str, usize>) -> usize {
    counter1.iter().fold(0, |acc, (key, val)| {
        acc + val * counter2.get(key).unwrap_or(&0)
    })
}

pub fn magnitude(counter: &HashMap<&str, usize>) -> f64 {
    counter.values().fold(0.0, |acc, &val| acc + (val * val) as f64).sqrt()
}
