from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate

from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain_community.document_loaders import GitLoader
from langchain_community.chat_models.ollama import ChatOllama


def invoke_chain(loader: GitLoader, llm: ChatOllama):
    map_template = """You are a software analyst tasked with generating functional software documentation for a specific codebase.
    You are given a piece of code from a larger codebase. Your task is to generate functional software documentation for this specific piece of code.
    Do not include the code itself in the documentation, but rather describe its functionality and purpose.

    Here is the code:
    {docs}

    Helpful Answer:
    """

    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    # Reduce
    reduce_template = """You are a software analyst tasked with generating functional software documentation for a specific codebase.
    You are given a collection of functional software documentation pieces generated from different parts of a larger codebase.
    Do not be redundant, do not give a title to the project.
    Your task is to summarize these pieces into a comprehensive document following the structure below:

    # Introduction and Overview

    ## Purpose
    Describe the objective of the document and what the reader can expect to gain from it.

    ## Scope
    Outline what the document covers and any limitations.

    ## Project Overview
    Provide a high-level summary of the project, including its main features and functionalities.

    ## Detailed Documentation
    Combine the functional documentation pieces in a logical order and format them into a cohesive section.

    Do not include code in the documentation and do not reference specific functions or classes,
    provide only high-level descriptions of the functionality and purpose of the code.
    Generate the response in markdown format respecting the headings and structure provided.

    This is the documentation to process: {docs}
    Helpful Answer:
    """

    reduce_prompt = PromptTemplate.from_template(reduce_template)

    # Run chain
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="docs"
    )

    # Combines and iteratively reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )

    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )

    docs = loader.load()
    split_docs = text_splitter.split_documents(docs)

    result = map_reduce_chain.invoke(split_docs)

    return result
