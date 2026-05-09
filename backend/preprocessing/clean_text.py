import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Download required NLTK resources
for resource in ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

STOP_WORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()


def get_wordnet_pos(treebank_tag: str) -> str:
    from nltk.corpus import wordnet
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def clean_text(text: str) -> str:
    """Full NLP pipeline matching the notebook preprocessing."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " ", text)     # URLs
    text = re.sub(r"<[^>]+>", " ", text)               # HTML tags
    text = re.sub(r"[^a-z\s]", " ", text)              # punctuation / digits
    text = re.sub(r"\s+", " ", text).strip()

    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

    pos_tags = pos_tag(tokens)
    tokens = [LEMMATIZER.lemmatize(t, get_wordnet_pos(pos)) for t, pos in pos_tags]

    return " ".join(tokens)
