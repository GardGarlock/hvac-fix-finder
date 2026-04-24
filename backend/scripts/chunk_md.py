import argparse
import os
import json
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

def process_hvac_manual(input_file, chunk_size, chunk_overlap):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    headers_to_split_on = [
        ("#", "H1"),
        ("##", "H2"),
        ("###", "H3"),
        ("####", "H4"),
        ("#####", "H5"),
        ("######", "H6"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False 
    )
    md_header_splits = markdown_splitter.split_text(content)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "---", "\n- ", "\n1. ", ". ", " ", ""]
    )

    final_chunks = text_splitter.split_documents(md_header_splits)

    for chunk in final_chunks:
        if chunk.metadata.get("H1") == "TABLE OF CONTENTS":
            del chunk.metadata["H1"]
        
        path = [v for k, v in chunk.metadata.items() if v]
        chunk.metadata["section_path"] = " > ".join(path)

    return final_chunks

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--size", type=int, default=1200)
    parser.add_argument("--overlap", type=int, default=150)
    parser.add_argument(
        "--save_path",
        default=None,
        help="Directory to write hvac_chunks.json (default: current working directory)",
    )
    args = parser.parse_args()

    chunks = process_hvac_manual(args.input, args.size, args.overlap)

    out_dir = args.save_path if args.save_path is not None else os.getcwd()
    os.makedirs(out_dir, exist_ok=True)
    output_file = os.path.join(out_dir, "hvac_chunks.json")
    with open(output_file, "w") as f:
        json.dump([{"content": c.page_content, "metadata": c.metadata} for c in chunks], f, indent=2)
    
    print(f"Processed {len(chunks)} chunks. Exported to {output_file}")
