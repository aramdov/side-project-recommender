from pathlib import Path
from langchain.document_loaders import GitLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Dict, List, Union
import re

class RepoProcessor:
    def __init__(self, base_path: str = "./temp_repos"):
        self.base_path = Path(base_path)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def process_repo(self, repo_url: str, repo_type: str = "curated_list"):
        """
        Process a repository based on its type
        repo_type: "curated_list" or "project_repo"
        """
        try:
            # Clone repo
            loader = GitLoader(
                clone_url=repo_url,
                branch="main",
                repo_path=str(self.base_path / repo_url.split('/')[-1])
            )
            
            if repo_type == "curated_list":
                return self._process_curated_list(loader, repo_url)
            else:
                return self._process_project_repo(loader, repo_url)
                
        except Exception as e:
            print(f"Error processing {repo_url}: {str(e)}")
            return []

    def _process_curated_list(self, loader: GitLoader, repo_url: str) -> List[Dict]:
        """Process repositories that are primarily curated lists"""
        # Focus on README and markdown files
        docs = loader.load()
        markdown_docs = [doc for doc in docs if doc.metadata["source"].endswith(('.md', '.MD'))]
        
        chunks = self.text_splitter.split_documents(markdown_docs)
        
        # Enrich with metadata
        for chunk in chunks:
            chunk.metadata.update({
                "repo_url": repo_url,
                "type": "curated_list",
                "content_type": "resource_list",
                # Extract any section headers or categories from the markdown
                "category": self._extract_category(chunk.text),
            })
        
        return chunks

    def _process_project_repo(self, loader: GitLoader, repo_url: str) -> List[Dict]:
        """Process repositories containing actual projects"""
        docs = loader.load()
        processed_chunks = []
        
        # First, process README for project overview
        readme_docs = [doc for doc in docs if "README" in doc.metadata["source"]]
        if readme_docs:
            readme_chunks = self.text_splitter.split_documents(readme_docs)
            for chunk in readme_chunks:
                chunk.metadata.update({
                    "repo_url": repo_url,
                    "type": "project_repo",
                    "content_type": "project_overview",
                })
            processed_chunks.extend(readme_chunks)
        
        # Then process key files for project structure
        for doc in docs:
            if self._is_key_file(doc.metadata["source"]):
                chunks = self.text_splitter.split_documents([doc])
                for chunk in chunks:
                    chunk.metadata.update({
                        "repo_url": repo_url,
                        "type": "project_repo",
                        "content_type": "code_sample",
                        "file_path": doc.metadata["source"],
                        "technology": self._detect_technology(doc.metadata["source"]),
                        "project_structure": self._extract_project_structure(doc.text)
                    })
                processed_chunks.extend(chunks)
        
        return processed_chunks

    def _is_key_file(self, filepath: str) -> bool:
        """Determine if a file contains important project information"""
        key_files = [
            'package.json', 'requirements.txt', 'setup.py',
            'docker-compose.yml', 'Dockerfile', 'assets', 'js', 'src',
            'main.py', 'index.js', 'app.py'
        ]
        return any(filepath.endswith(file) for file in key_files)

    def _detect_technology(self, filepath: str) -> List[str]:
        """Detect technologies based on file extensions and content"""
        tech_map = {
        '.py': ['Python'],
        '.js': ['JavaScript'],
        '.jsx': ['JavaScript', 'React'],
        '.ts': ['TypeScript'],
        '.tsx': ['TypeScript', 'React'],
        '.java': ['Java'],
        '.rb': ['Ruby'],
        '.php': ['PHP'],
        '.go': ['Go'],
        '.rs': ['Rust'],
        '.cpp': ['C++'],
        '.cs': ['C#'],
        '.html': ['HTML'],
        '.css': ['CSS'],
        '.json': ['JSON'],
        '.yml': ['YAML'],
        '.yaml': ['YAML'],
        '.xml': ['XML'],
        '.sh': ['Shell'],
        '.dockerfile': ['Docker'],
        'Dockerfile': ['Docker']
        }

        extension = filepath.split('.')[-1]
        if extension in tech_map:
            return tech_map[extension]
        elif filepath.endswith('Dockerfile'):
            return ['Docker']
        else:
            return ['Unknown']
        

    def _extract_project_structure(self, content: str) -> Dict:
        """Extract key information about project structure"""
        project_structure = {}
        lines = content.split('\n')
        
        # Track current directory
        current_dir = project_structure
        dir_stack = [current_dir]
        
        for line in lines:
            # Match directories
            dir_match = re.match(r'^\s*([\w\-/]+):$', line)
            if dir_match:
                dir_name = dir_match.group(1)
                new_dir = {}
                current_dir[dir_name] = new_dir
                dir_stack.append(new_dir)
                current_dir = new_dir
                continue
            
            # Match files
            file_match = re.match(r'^\s*([\w\-.]+)$', line)
            if file_match:
                file_name = file_match.group(1)
                current_dir[file_name] = None
                continue
            
            # Handle indentation level changes
            if line.strip() == '':
                dir_stack.pop()
                if dir_stack:
                    current_dir = dir_stack[-1]
        
        return project_structure
    

    def _extract_category(self, content: str) -> List[str]:
        """Extract categories from README content"""
        categories = []
        
        # Regular expressions for headings and bullet points
        heading_pattern = re.compile(r'^(#{1,3})\s*(.+)')
        bullet_pattern = re.compile(r'^\s*[-*]\s*(.+)')
        
        lines = content.split('\n')
        
        for line in lines:
            # Match headings
            heading_match = heading_pattern.match(line)
            if heading_match:
                categories.append(heading_match.group(2).strip())
                continue
            
            # Match bullet points
            bullet_match = bullet_pattern.match(line)
            if bullet_match:
                categories.append(bullet_match.group(1).strip())
        
        return categories
    
