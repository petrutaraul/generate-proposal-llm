# 📝 Generator Script

Welcome to the Generator Script repository! This Python script processes a client request document to generate a detailed PDF proposal. It's designed to handle various document formats and extract relevant information for your proposals. Let's get started! 🚀

## 📦 Installation

To get started, clone the repository and navigate into the directory:

```sh
git clone https://github.com/petrutaraul/generate-proposal-llm
cd generate-proposal-llm
```

## 🐍 Setting Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment using the following commands:

For Windows:

```sh
python -m venv generate-proposal-llm
generate-proposal-llm\Scripts\activate
```

For macOS and Linux:

```sh
python3 -m venv generate-proposal-llm
source generate-proposal-llm/bin/activate
```

## 📜 Install Dependencies

Once the virtual environment is activated, install the required dependencies:

```sh
pip install -r requirements.txt
```

## 🐙 Install Ollama

This script uses Ollama. Follow these steps to install it:

1. Visit the [Ollama website](https://ollama.ai/) to download the installer for your operating system.
2. Follow the installation instructions provided on the website.
3. Verify the installation by running:

```sh
ollama --version
```

## 🚀 Running the Script

With the dependencies installed, you can run the script using:

```sh
python generator.py <client_request_file>
```

Replace `<client_request_file>` with the path to the client request file.

## 📋 Requirements

The `requirements.txt` file includes all necessary dependencies. Here they are for reference:

```
requests
python-docx
PyPDF2
reportlab
ollama
```

## 🤔 How It Works

1. **Reading File Content**: The script can read .docx, .pdf, and .txt files, extracting their text content.
2. **Generating Document**: Using Ollama's AI, it generates a detailed project proposal based on the client's request.
3. **Creating PDF**: The proposal is formatted into a PDF using ReportLab, with support for Romanian diacritics.

## 🧪 Example

Here's how you might run the script:

```sh
python generator.py client_request.docx
```

This will read the `client_request.docx` file and generate a detailed proposal saved as a PDF.
