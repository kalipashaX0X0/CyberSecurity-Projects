# install_libraries.py
import subprocess
import nltk

def install(package):
    subprocess.check_call(["pip", "install", package])

# Install required libraries
libraries = ["pandas", "nltk", "scikit-learn"]

for lib in libraries:
    print(f"Installing {lib}...")
    install(lib)

# Download NLTK resources
print("\nDownloading NLTK resources...")
nltk.download('punkt')       # Tokenizer models
nltk.download('stopwords')   # Stop words list
nltk.download('wordnet')     # WordNet lemmatizer data

print("\nSetup complete! All required libraries and resources have been installed.")
