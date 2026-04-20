from typing import List
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


# Ferramenta para ler um arquivo
@mcp.tool(
    name="read_doc_contents",
    description="Read the content of a document and return as a string."
)
def read_document(
    doc_id: str = Field(description = "The id of the document to read.")
):
    # Verifica se o documento existe. Se não existir, devolve um erro
    if doc_id not in docs:
        raise ValueError(f"Doc with doc_id {doc_id} not found.")
    # Retorna o conteúdo do documento
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc_contents",
    description="Edit a document by replacing a string in the documents content with a new string."
)
def edit_document(
    doc_id: str = Field(description="The id of the document that will be edited."),
    old_str: str = Field(description="The text to replace. Must match exactly, including white spaces."),
    new_str: str = Field(description="The new text to insert in place of the old text.")
):
    # Verifica se o documento existe. Se não existir, devolve um erro
    if doc_id not in docs:
        raise ValueError(f"Doc with doc_id {doc_id} not found.")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# Retorna todos os ids dos documentos
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with doc_id {doc_id} not found.")
    return docs[doc_id]


# Prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrites the content of the document in markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> List[base.Message]:
    if doc_id not in docs:
        raise ValueError(f"Doc with doc_id {doc_id} not found.")
    prompt = f"""
        Your goal is to reformat a document to be written with markdown syntax.

        The id of the document you need to reformat is:
        <document_id>
        {doc_id}
        </document_id>

        Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
        Use the 'edit_document' tool to edit the document. After the document has been reformatted...
        """
    return [
        base.UserMessage(prompt)
    ]

# TODO: Write a prompt to summarize a doc
@mcp.prompt(
    name="summary",
    description="Summarize a document."
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize")
) -> List[base.Message]:
    if doc_id not in docs:
        raise ValueError(f"Doc with doc_id {doc_id} not found.")
    prompt = f"""
        Your goal is to summarize a document.
        
        The id of the document you need to summarize is:
        <document_id>
        {doc_id}
        </document_id>
        
        Provide a concise summary of the document's main points and key information.
        """
    return [
        base.UserMessage(prompt)
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
