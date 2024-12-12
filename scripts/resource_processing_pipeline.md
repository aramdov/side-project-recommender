graph TB
    A[Resource URLs] --> B{Resource Type}
    B -->|GitHub| C[GitHub Processor]
    B -->|Website| D[Website Processor]
    
    C --> E[Document Chunking]
    D --> E
    
    E --> F[Metadata Enrichment]
    F --> G[Embedding Generation]
    G --> H[Vector DB Upload]
    
    subgraph "Metadata Enrichment"
    I[Project Properties] --> F
    J[Technology Detection] --> F
    K[Difficulty Estimation] --> F
    end
    
    H --> L[(Pinecone DB)]