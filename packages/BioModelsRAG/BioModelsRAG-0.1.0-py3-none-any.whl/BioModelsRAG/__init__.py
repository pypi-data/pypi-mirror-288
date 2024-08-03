__version__ = "0.1.0"
__author__ = "Bhavyahshree Navaneetha Krishnan"

#Install the following packages in a virtual environment using pip install
#pip install langchain
#pip install chromadb
#pip install sentence_transformers
#pip install langchain_text_splitters
#pip install ollama


from langchain_text_splitters import CharacterTextSplitter
import os
import chromadb
from chromadb.utils import embedding_functions
import ollama

from splitBioModels import final_items
from createVectorDB import collection
from createDocuments import documents

__all__ = ['splitBioModels', 'final_items', 'createVectorDB', 'collection', 'documents']

#need to figure out the file path issue

#Todolist:
#1. Create a public drive link that all of the BioModels will be loaded into and a way for the code to access it 
#2. Create a way for the embeddings + text generations to be stored locally on the computer and accessed when the program is opened more than once (initialize it once and then never need to do it again) (automatic updating?)
#3. Finish setup.py file

#consider creating a website and a Python package
#also update github at some point
#consider a zip file for organizing the models