import warnings
import openai
import os
import faiss
import pdfplumber
import numpy as np
from docx import Document
import logging
import time
import tiktoken
import platform
import zipfile
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from odf.opendocument import load
from odf.text import P
import json
import argparse
import importlib.metadata
import diskcache as dc
import markdown2
import subprocess
import webbrowser
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(level=logging.INFO)
cache = dc.Cache(os.path.join(os.path.expanduser('~'), 'docusearch_cache'))
tokenizer = tiktoken.get_encoding('cl100k_base')

warnings.filterwarnings("ignore", category=UserWarning, module="ebooklib.epub")
warnings.filterwarnings("ignore", category=FutureWarning, module="ebooklib.epub")

def extract_text_from_pdf(pdf_path):
    text = ''
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
    except pdfplumber.pdfparser.PDFSyntaxError:
        logging.error(f"Error processing PDF file: {pdf_path}. The file is not a valid PDF.")
    return text

def extract_text_from_docx(docx_path):
    return '\n'.join([para.text for para in Document(docx_path).paragraphs])

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_odt(odt_path):
    doc = load(odt_path)
    return '\n'.join(node.data for paragraph in doc.getElementsByType(P) for node in paragraph.childNodes if node.nodeType == 3 or (node.nodeType == 1 and node.firstChild))

def extract_text_from_html_zip(zip_path):
    text = ''
    with zipfile.ZipFile(zip_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith('.html'):
                with z.open(filename) as f:
                    text += BeautifulSoup(f, 'html.parser').get_text() + '\n'
    return text

def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    return '\n'.join(BeautifulSoup(item.get_body_content(), 'html.parser').get_text() + '\n' for item in book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT)

def split_text_into_chunks(text, max_tokens):
    tokens = tokenizer.encode(text)
    return [tokenizer.decode(tokens[i:i + max_tokens]) for i in range(0, len(tokens), max_tokens)]

def generate_embeddings(text, api_key, model="text-embedding-ada-002"):
    openai.api_key = api_key
    chunks = split_text_into_chunks(text, max_tokens=2048)
    embeddings = [openai.Embedding.create(input=chunk, model=model)['data'][0]['embedding'] for chunk in chunks]
    return np.mean(embeddings, axis=0)

def get_new_files(directory, cached_files):
    return set(os.listdir(directory)) - cached_files

def read_documents(directory, api_key):
    documents, metadatas, ids, embeddings, unsupported_files = [], [], [], [], []
    if directory in cache:
        logging.info(f"Loading documents from cache for directory: {directory}")
        cached_data = cache[directory]
        cached_files = set(metadata["source"] for metadata in cached_data["metadatas"])
        new_files = get_new_files(directory, cached_files)

        if not new_files:
            return cached_data["documents"], cached_data["metadatas"], cached_data["ids"], cached_data["embeddings"], unsupported_files

        documents, metadatas, ids, embeddings = cached_data["documents"], cached_data["metadatas"], cached_data["ids"], list(cached_data["embeddings"])
    else:
        logging.info(f"Processing documents in directory: {directory}")
        new_files = set(os.listdir(directory))

    extractors = {
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
        ".txt": extract_text_from_txt,
        ".odt": extract_text_from_odt,
        ".zip": extract_text_from_html_zip,
        ".epub": extract_text_from_epub,
    }

    for filename in new_files:
        ext = os.path.splitext(filename)[1].lower()
        extractor = extractors.get(ext)
        if not extractor:
            unsupported_files.append(filename)
            continue

        text = extractor(os.path.join(directory, filename))
        if not text:
            logging.warning(f"Skipped empty or invalid file: {os.path.join(directory, filename)}")
            continue

        documents.append(text)
        metadata = {"source": filename}
        metadatas.append(metadata)
        doc_id = os.path.splitext(filename)[0]
        ids.append(doc_id)

        document_embedding = generate_embeddings(text, api_key)
        if document_embedding is None:
            return None, None, None, None, unsupported_files
        embeddings.append(document_embedding)

    embeddings = np.array(embeddings)
    cache[directory] = {"documents": documents, "metadatas": metadatas, "ids": ids, "embeddings": embeddings}

    return documents, metadatas, ids, embeddings, unsupported_files

def clear_cache():
    cache.clear()
    logging.info("Cache cleared successfully.")

def split_document(document, max_tokens=4096):
    return split_text_into_chunks(document, max_tokens=max_tokens)

def query_chunk(chunk_num, chunk, question, api_key, model="gpt-4", short_response=False, document_type="default"):
    openai.api_key = api_key
    max_completion_tokens = 512 if not short_response else 128
    max_input_tokens = 8192 - max_completion_tokens
    chunk = split_text_into_chunks(chunk, max_input_tokens)[0]

    if document_type == "financial":
        prompt = f"Document chunk {chunk_num}:\n{chunk}\n\nQuestion: {question}\n\nProvide a detailed answer in tabular format and cite sentences from the document. Make sure your response is extremely well structured so I can parse the text, identify potential table structures, and then organize the data into a spreadsheet form. Make your response pretty using bolding, lists, italics, etc." if not short_response else f"Document chunk {chunk_num}:\n{chunk}\n\nQuestion: {question}\n\nProvide a concise answer in tabular format and cite sentences from the document. Make sure your response is extremely well structured so I can parse the text, identify potential table structures, and then organize the data into a spreadsheet form. Make your response pretty using bolding, lists, italics, etc."
    else:
        prompt = f"Document chunk {chunk_num}:\n{chunk}\n\nQuestion: {question}\n\nProvide a detailed answer and cite sentences from the document. Make your response pretty using bolding, lists, italics, etc." if not short_response else f"Document chunk {chunk_num}:\n{chunk}\n\nQuestion: {question}\n\nProvide a concise answer and cite sentences from the document. Make your response pretty using bolding, lists, italics, etc."

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_completion_tokens
    )
    return chunk_num, response.choices[0].message['content']

def get_answers_with_citations(question, document_chunks, api_key, model="gpt-4", short_response=False, document_type="default"):
    all_evidence = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(query_chunk, i+1, chunk, question, api_key, model, short_response, document_type) for i, chunk in enumerate(document_chunks)]
        for future in as_completed(futures):
            chunk_num, answer = future.result()
            all_evidence.append((chunk_num, answer))
    return all_evidence

def combine_answers_with_citations(evidence_list):
    combined_answer = ""
    citations = []
    for chunk_num, answer in evidence_list:
        combined_answer += f"\n{answer}"
        sentences = [sent.strip() for sent in answer.split('.') if any(word in sent for word in answer.split())]
        citations.extend(sentences)
    return combined_answer, citations

def query_index(query_embedding, index, metadatas, documents, embeddings, n_results=1):
    query_embedding = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_embedding, n_results)
    return [{'distance': distances[0][i], 'metadata': metadatas[indices[0][i]], 'document': documents[indices[0][i]], 'embedding': embeddings[indices[0][i]]} for i in range(n_results)]

def create_faiss_index(embeddings, embedding_dim):
    if embeddings.shape[0] < 256:
        index = faiss.IndexFlatL2(embedding_dim)
    else:
        nlist = max(1, min(100, embeddings.shape[0] // 4))
        quantizer = faiss.IndexFlatL2(embedding_dim)
        index = faiss.IndexIVFPQ(quantizer, embedding_dim, nlist, 8, 8)
        index.train(embeddings)
    index.add(embeddings)
    return index

def normalize_folder_path(folder_path):
    user_os = platform.system().lower()
    if 'windows' in user_os:
        return folder_path.replace('/mnt/c', 'C:').replace('/', '\\') if folder_path.startswith('/mnt/c') else folder_path
    return folder_path.replace('C:', '/mnt/c').replace('\\', '/') if folder_path[1] == ':' else folder_path.replace('\\', '/')

def identify_relevant_chunks(query_text, document_chunks, api_key, model="gpt-4"):
    relevant_chunks = []

    def process_chunk(chunk_num, chunk):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Document chunk {chunk_num}:\n{chunk}\n\nQuestion: Does this chunk contain any information relevant to the question: {query_text}?\n\nAnswer 'yes' if this chunk contains relevant information, otherwise answer 'no'. If there is even a single phrase that may be relevant, mark the chunk as 'yes'."}
            ],
            max_tokens=5
        )
        return chunk_num, response.choices[0].message['content'].strip().lower()

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, i+1, chunk) for i, chunk in enumerate(document_chunks)]
        for future in as_completed(futures):
            chunk_num, answer = future.result()
            if answer == "yes":
                relevant_chunks.append((chunk_num, document_chunks[chunk_num - 1]))
    return relevant_chunks

def process_best_matching_document(query_text, api_key, folder_path, model="gpt-4", short_response=False, document_type="default"):
    folder_path = normalize_folder_path(folder_path)
    start_time = time.time()
    documents, metadatas, ids, embeddings, unsupported_files = read_documents(folder_path, api_key)
    if documents is None:
        return None, None, unsupported_files
    processing_time = time.time() - start_time
    logging.info(f"Document processing time: {processing_time:.2f} seconds")

    embedding_dim = embeddings.shape[1]
    index = create_faiss_index(np.array(embeddings).astype('float32'), embedding_dim)

    query_embedding_start_time = time.time()
    query_embedding = generate_embeddings(query_text, api_key)
    if query_embedding is None:
        return None, None, unsupported_files
    query_embedding_time = time.time() - query_embedding_start_time
    logging.info(f"Query embedding generation time: {query_embedding_time:.2f} seconds")

    results = query_index(query_embedding, index, metadatas, documents, embeddings)
    best_result = results[0]
    best_document = best_result['document']
    best_metadata = best_result['metadata']['source']

    filter_chunks_start_time = time.time()
    document_chunks = split_document(best_document)
    relevant_chunks = identify_relevant_chunks(query_text, document_chunks, api_key, model)
    filter_chunks_query_time = time.time() - filter_chunks_start_time
    logging.info(f"Filter chunks time: {filter_chunks_query_time:.2f} seconds")

    gpt_response_start_time = time.time()
    evidence_list = get_answers_with_citations(query_text, [chunk for _, chunk in relevant_chunks], api_key, model, short_response, document_type)
    gpt_response_time = time.time() - gpt_response_start_time
    logging.info(f"GPT response generation time: {gpt_response_time:.2f} seconds")

    answer, citations = combine_answers_with_citations(evidence_list)
    querying_time = time.time() - start_time
    logging.info(f"Total querying time: {querying_time:.2f} seconds")

    return best_metadata, answer, unsupported_files

def process_query(query_text, api_key, folder_path, model="gpt-4", short_response=False, document_type="default", save_to_json=True):
    if not query_text or not api_key or not folder_path:
        raise ValueError("Query text, API key, and folder path are required")

    folder_path = normalize_folder_path(folder_path)
    if not os.path.exists(folder_path):
        logging.error(f"The folder path does not exist: {folder_path}")
        raise FileNotFoundError(f"The folder path does not exist: {folder_path}")

    best_metadata, answer, unsupported_files = process_best_matching_document(query_text, api_key, folder_path, model, short_response, document_type)
    if best_metadata is None:
        raise ValueError("Invalid API key")

    response = {"document_source": best_metadata, "answer": answer}
    if unsupported_files:
        response["warning"] = f"The following files are unsupported and were not processed: {', '.join(unsupported_files)}"

    if save_to_json:
        with open("data.json", "w") as json_file:
            json.dump(response, json_file)

    return best_metadata, answer, unsupported_files

def open_in_browser(document, answer, wsl=False):
    html_content = markdown2.markdown(answer, extras=["tables"])
    output_file_path = "output.html"

    html_with_style = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Query Result</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5; margin: 20px; line-height: 1.6; color: #333; }}
            h1, h2, h3, h4, h5, h6 {{ color: #0b736e; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #0b736e; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            tr:hover {{ background-color: #ddd; }}
            code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; color: #c7254e; }}
            pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; color: #c7254e; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
            a {{ color: #4CAF50; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{document}</h1>
            <h2>Answer:</h2>
            {html_content}
        </div>
    </body>
    </html>
    """

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_with_style)
    open_file_in_browser(output_file_path, wsl)
    logging.info(f"HTML file created and opened: {output_file_path}")

def open_file_in_browser(file_path, wsl=False):
    user_os = platform.system().lower()
    if wsl:
        windows_path = os.path.abspath(file_path).replace('/mnt/c', 'C:').replace('/', '\\')
        subprocess.run(['explorer.exe', windows_path])
        return

    if 'windows' in user_os:
        webbrowser.open('file://' + os.path.realpath(file_path))
    elif 'darwin' in user_os:
        subprocess.run(['open', file_path])
    else:
        subprocess.run(['xdg-open', file_path])

def get_answer_from_context(context, api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4", short_response=False, document_type="default"):
    openai.api_key = api_key
    max_completion_tokens = 512 if not short_response else 128

    if document_type == "financial":
        prompt = f"{context}\n\nProvide a detailed answer in tabular format and cite sentences from the previous answer. Make sure your response is extremely well structured so I can parse the text, identify potential table structures, and then organize the data into a spreadsheet form" if not short_response else f"{context}\n\nProvide a concise answer in tabular format and cite sentences from the previous answer. Make sure your response is extremely well structured so I can parse the text, identify potential table structures, and then organize the data into a spreadsheet form."
    else:
        prompt = f"{context}\n\nProvide a detailed answer and cite sentences from the previous answer." if not short_response else f"{context}\n\nProvide a concise answer and cite sentences from the previous answer."

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_completion_tokens
    )
    return response.choices[0].message['content']

def read_single_document(directory, document_name):
    file_path = os.path.join(directory, document_name)

      # Check if the document is in the cache
    if directory in cache:
        cached_data = cache[directory]
        for metadata, doc in zip(cached_data["metadatas"], cached_data["documents"]):
            if metadata["source"] == document_name:
                logging.info(f"Loaded document from cache: {document_name}")
                return doc, None
            
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return None, f"File not found: {file_path}"

    extractors = {
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
        ".txt": extract_text_from_txt,
        ".odt": extract_text_from_odt,
        ".zip": extract_text_from_html_zip,
        ".epub": extract_text_from_epub,
    }

    ext = os.path.splitext(document_name)[1].lower()
    extractor = extractors.get(ext)
    if not extractor:
        logging.error(f"Unsupported file format: {document_name}")
        return None, f"Unsupported file format: {document_name}"

    text = extractor(file_path)
    if not text:
        logging.warning(f"Skipped empty or invalid file: {file_path}")
        return None, f"Skipped empty or invalid file: {file_path}"

    return text, None

def follow_up(follow_up_question, api_key=os.getenv("OPENAI_API_KEY"), json_file_path="data.json", model="gpt-4", short_response=False, document_type="default", folder_path=None):
    follow_up_start_time = time.time()

    with open(json_file_path, "r") as json_file:
        saved_data = json.load(json_file)

    document_source = saved_data["document_source"]
    previous_answer = saved_data["answer"]
    context = f"Previous answer: {previous_answer}\n\nFollow-up question: {follow_up_question}"

    if folder_path:
        folder_path = normalize_folder_path(folder_path)
        single_start_time = time.time()
        document_text, error = read_single_document(folder_path, document_source)
        single_time = time.time() - single_start_time
        logging.info(f"Document processing time: {single_time:.2f} seconds")

        filter_chunks_start_time = time.time()
        document_chunks = split_document(document_text)
        relevant_chunks = identify_relevant_chunks(context, document_chunks, api_key, model)
        filter_chunks_query_time = time.time() - filter_chunks_start_time
        logging.info(f"Filter chunks time: {filter_chunks_query_time:.2f} seconds")

        gpt_response_start_time = time.time()
        evidence_list = get_answers_with_citations(context, [chunk for _, chunk in relevant_chunks], api_key, model, short_response, document_type)
        gpt_response_time = time.time() - gpt_response_start_time
        logging.info(f"GPT response generation time: {gpt_response_time:.2f} seconds")

        answer, citations = combine_answers_with_citations(evidence_list)
    else:
        gpt_response_start_time = time.time()
        answer = get_answer_from_context(context, api_key, model, short_response, document_type)
        gpt_response_time = time.time() - gpt_response_start_time
        logging.info(f"GPT response generation time: {gpt_response_time:.2f} seconds")

    follow_up_query_time = time.time() - follow_up_start_time
    logging.info(f"Follow up query: {follow_up_query_time:.2f} seconds")

    return answer

def main():
    parser = argparse.ArgumentParser(description='Docusearch Command Line Interface')
    parser.add_argument('--version', action='store_true', help='Show the version of docusearch')
    parser.add_argument('--clear-cache', action='store_true', help='Clear cache of documents')
    args = parser.parse_args()

    if args.version:
        version = importlib.metadata.version('docusearch')
        print(f"Docusearch {version}")

if __name__ == '__main__':
    main()
