# Project Idea Generator: Inspiring the Next Generation of Developers 🚀

After some mentoring of CS students and junior developers, I've noticed a persistent challenge: the struggle to bridge the gap between learning and doing. While tutorials abound, finding that *ideal* side project—one that's both motivating and skill-building—remains surprisingly difficult. This tool aims to change that.

## Vision & Purpose 💡

This AI-powered project recommender doesn't just match skills to projects; it understands the delicate balance between comfort and growth. Through my experience in both education and software development, I've learned that the best projects aren't necessarily the most complex ones—they're the ones that keep you coding at 2 AM because you're too excited to sleep.

Our system leverages:
- RAG (Retrieval Augmented Generation) for contextual understanding
- Claude's capabilities for nuanced project suggestions
- Pinecone's vector database for efficient knowledge retrieval

## Getting Started 🌟

### Prerequisites
- Python 3.9+
- A Pinecone API key
- An Anthropic API key
- Future version can use OpenAI API key.

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/aramdov/project-recommender.git
cd project-recommender

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

### Running the Application
```bash
streamlit run frontend/pages/Home.py
```

## Project Structure 📁

```
project_root/
├── backend/           # Core business logic
├── frontend/         # Streamlit interface
├── data/            # Knowledge base and embeddings
├── tests/           # Test suites
├── config/          # Configuration management
└── scripts/         # Utility scripts
```

### Key Components
- **Vector Store**: Pinecone integration for efficient project template storage and retrieval
- **Document Processor**: Handles resume parsing and text extraction
- **Recommendation Engine**: Combines RAG with Claude for personalized suggestions

## Development Philosophy 🤔

I've structured this project with both immediate utility and future scalability in mind. While Streamlit serves as our MVP frontend, the clean separation between backend and frontend components makes future transitions (say, to Next.js) more manageable.

Some key decisions I've made:
1. Using RAG over pure semantic search for richer context understanding
2. Choosing Pinecone for its reliability and free tier accessibility
3. Implementing strict typing and clean architecture from day one

## Future Roadmap 🗺️

- [ ] Enhanced multi-modal document processing
- [ ] Learning resource integration
- [ ] Community-driven project template contributions
- [ ] Potential Next.js frontend migration

## Contributing 🤝

Whether you're a student who's used the tool, a mentor with project ideas to share, or a developer with technical insights, your contributions are welcome! Check out our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Local Development 💻

```bash
# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ to help developers find their next exciting project*