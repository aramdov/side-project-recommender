# # scripts/initialize_vectordb.py
# import os
# from dotenv import load_dotenv
# from typing import List, Dict, Any
# from dataclasses import dataclass
# import logging

# @dataclass
# class ProcessingConfig:
#     chunk_size: int = 500
#     chunk_overlap: int = 50
#     embedding_dimension: int = 1536  # OpenAI's default
#     text_splitter_separators: List[str] = field(
#         default_factory=lambda: ["\n\n", "\n", " ", ""]
#     )
    
# class VectorDBInitializer:
#     def __init__(self, config: ProcessingConfig):
#         self.config = config
#         self._setup_logging()
#         self._initialize_pinecone()
        
#     def process_resources(self, resources: List[str]):
#         """Main processing pipeline for initializing vector DB"""
#         for resource in resources:
#             try:
#                 if self._is_github_repo(resource):
#                     chunks = self._process_github_repo(resource)
#                 else:
#                     chunks = self._process_website(resource)
                
#                 # Enrich chunks with metadata
#                 enriched_chunks = self._enrich_chunks_with_metadata(chunks)
                
#                 # Upload to Pinecone
#                 self._upload_to_pinecone(enriched_chunks)
                
#             except Exception as e:
#                 logging.error(f"Error processing {resource}: {str(e)}")
                
#     def _enrich_chunks_with_metadata(self, chunks: List[Document]) -> List[Document]:
#         """Add metadata to each chunk for context preservation"""
#         for chunk in chunks:
#             # Base metadata that should be in every chunk
#             base_metadata = {
#                 "source": chunk.metadata.get("source"),
#                 "source_type": "github" if "github.com" in chunk.metadata.get("source", "") else "website",
#                 "chunk_index": chunk.metadata.get("chunk_index"),
#                 "total_chunks": chunk.metadata.get("total_chunks"),
#                 "document_title": self._extract_title(chunk),
#             }
            
#             # Enrich with detected properties
#             enriched_metadata = {
#                 **base_metadata,
#                 **self._detect_project_properties(chunk.text),
#                 **self._detect_technologies(chunk.text),
#                 "difficulty_level": self._estimate_difficulty(chunk.text)
#             }
            
#             chunk.metadata.update(enriched_metadata)
            
#         return chunks
    
#     def _detect_project_properties(self, text: str) -> Dict[str, Any]:
#         """Detect project properties from chunk text"""
#         return {
#             "project_type": self._classify_project_type(text),
#             "estimated_time": self._estimate_time_commitment(text),
#             "prerequisites": self._extract_prerequisites(text),
#             "learning_outcomes": self._extract_learning_outcomes(text)
#         }

# # Usage script
# if __name__ == "__main__":
#     load_dotenv()
    
#     config = ProcessingConfig(
#         chunk_size=500,
#         chunk_overlap=50
#     )
    
#     resources = [
#         "https://github.com/The-Cool-Coders/Project-Ideas-And-Resources",
#         "https://github.com/e2b-dev/awesome-ai-agents",
#         # ... more resources
#     ]
    
#     initializer = VectorDBInitializer(config)
#     initializer.process_resources(resources)