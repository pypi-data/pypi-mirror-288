# NeuralNet

## Overview

**NeuralNet** is a high-performance, Rust-based library designed for fast retrieval and generation (RAG) tasks. Leveraging Rust's efficiency, NeuralNet delivers rapid, reliable, and intelligent contextual processing capabilities, making it ideal for applications requiring quick information retrieval and seamless response generation.

## Features

- **Superfast Performance**: Built using Rust for optimal speed and efficiency.
- **Flexible Contextual Processing**: Supports complex RAG operations with minimal latency.
- **Easy Integration**: Simple Python bindings for seamless use in Python projects.
- **Open Source**: Licensed under the MIT License, allowing you to use, modify, and distribute freely.

## Installation

To use NeuralNet in your Python projects, follow these steps:

1. **Install the Python Package**

   First, install the package from PyPI:

   ```bash
   pip install NeuralNet

## Usage
Here’s the simple code to utilize in your Python code:

```bash

    import neuralnet as net
    
    def test_rust_functions():
        urls = ["https://botpress.com/blog/what-is-an-ai-agent"]
        texts = net.extract_texts(urls)
        print("Extracted texts:", texts)
    
        query = "how scaling support works"
        response = net.generate_response(query, texts)
        print("Generated response:", response)
    
    if __name__ == "__main__":
        test_rust_functions()

```
## Available Functions
`retrieve(query: str, documents: List[str]) -> str: Takes a query and a list of documents, returning the most relevant document based on contextual similarity.


## Contributing
We welcome contributions to NeuralNet! If you have suggestions, bug reports, or would like to contribute code, please follow these steps:

- **Fork the repository on GitHub.
- **Create a new branch for your changes.
- **Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact [Dhruv Kumar](dhruvkumar9115@gmail.com).