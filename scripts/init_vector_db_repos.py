



REPOS = {
    "curated_lists": [
        "https://github.com/The-Cool-Coders/Project-Ideas-And-Resources",
        # ... more curated list repos
    ],
    "project_repos": [
        "https://github.com/username/javascript-mini-projects",
        # ... more project repos
    ]
}

# Main ingestion script
def main():
    processor = RepoProcessor()
    
    all_documents = []
    
    # Process curated lists
    for repo_url in REPOS["curated_lists"]:
        documents = processor.process_repo(repo_url, "curated_list")
        all_documents.extend(documents)
    
    # Process project repos
    for repo_url in REPOS["project_repos"]:
        documents = processor.process_repo(repo_url, "project_repo")
        all_documents.extend(documents)
    
    # Upload to Pinecone
    pinecone_uploader = PineconeManager(...)
    pinecone_uploader.upload_documents(all_documents)