
import sys
import pickle
import numpy as np
from pathlib import Path

MODEL_DIR = Path(__file__).parent

def _generate_demo_data(texts, labels):
    """Generate synthetic demo data for demonstration purposes."""
    fake_samples = [
        "SHOCKING: Scientists HIDE the truth about vaccines causing mind control in children confirmed by doctors",
        "Breaking: President secretly meeting with aliens at Area 51, whistleblower reveals classified documents",
        "EXPOSED: Big Pharma suppressing natural cure for cancer that grows in your backyard",
        "You won't believe what they don't want you to know about the moon landing hoax",
        "URGENT: Global elite planning massive population reduction through chemtrails and 5G towers",
        "Scientists discover that the Earth is actually hollow and there's a civilization inside confirmed sources say",
        "Breaking news: Government admits to using weather control machines to cause floods and droughts",
        "BOMBSHELL: Mainstream media caught completely fabricating climate change statistics new study reveals",
        "Exclusive: Famous actor secretly working for deep state shadow government exposed by insider",
        "MUST READ: How microchips in your phone are monitoring your thoughts and sending data to Google",
        "Revealed: Water fluoridation is a mind control experiment that has been going on for decades",
        "Shock report: Thousands of children disappearing every year for secret rituals authorities ignore",
        "WAKE UP: The moon is actually an artificial satellite placed there by ancient aliens millions of years ago",
        "Exclusive insider reveals that elections have been rigged for 50 years using special software",
        "Scientists who questioned climate change found dead mysterious circumstances government cover up",
    ] * 10

    real_samples = [
        "The Federal Reserve announced a quarter-point interest rate increase citing continued economic growth",
        "Researchers at MIT have developed a new battery technology that could double electric vehicle range",
        "The United Nations Security Council met Thursday to discuss the ongoing humanitarian crisis",
        "Apple reported quarterly earnings exceeding analyst expectations with strong iPhone sales in Asia",
        "A new study published in the New England Journal of Medicine shows improved outcomes for cancer patients",
        "Congress passed the infrastructure bill after months of negotiations between both political parties",
        "NASA's James Webb Space Telescope captured new images of distant galaxies formed shortly after the Big Bang",
        "The World Health Organization updated its guidelines on antibiotic resistance prevention measures",
        "European Union leaders agreed on new climate targets aiming for carbon neutrality by 2050",
        "Economists at the IMF revised global growth forecasts upward citing strong consumer spending data",
        "The Supreme Court issued a ruling on voting rights that will affect upcoming state elections",
        "Technology companies reported record profits driven by cloud computing and artificial intelligence services",
        "Climate scientists published findings showing accelerated glacial melting in the Arctic Circle region",
        "The Federal Aviation Administration approved new drone delivery regulations for urban areas",
        "International trade negotiations concluded with a new agreement on tariffs between major economies",
    ] * 10

    texts.extend(fake_samples)
    labels.extend([0] * len(fake_samples))
    texts.extend(real_samples)
    labels.extend([1] * len(real_samples))
    print(f" Demo dataset: {len(texts)} samples")




# Try to load real datasets first
data_dir = Path(__file__).parent.parent / "datasets"

# Vos fichiers datasets
fake_csv_1 = data_dir / "BuzzFeed_fake_news_content.csv"
fake_csv_2 = data_dir / "PolitiFact_fake_news_content.csv"

true_csv_1 = data_dir / "BuzzFeed_real_news_content.csv"
true_csv_2 = data_dir / "PolitiFact_real_news_content.csv"

texts, labels = [], []

if (
    fake_csv_1.exists() and fake_csv_2.exists()
    and true_csv_1.exists() and true_csv_2.exists()
):

    import pandas as pd
    print("\n Loading datasets...")

    # Charger fake news
    df_fake_1 = pd.read_csv(fake_csv_1)
    df_fake_2 = pd.read_csv(fake_csv_2)

    # Charger real news
    df_true_1 = pd.read_csv(true_csv_1)
    df_true_2 = pd.read_csv(true_csv_2)

    # Fusionner
    df_fake = pd.concat([df_fake_1, df_fake_2], ignore_index=True)
    df_true = pd.concat([df_true_1, df_true_2], ignore_index=True)

    # Labels
    df_fake["label"] = 0
    df_true["label"] = 1

    for df in [df_fake, df_true]:

        # Détection colonnes
        title_col = "title" if "title" in df.columns else df.columns[0]

        if "text" in df.columns:
            text_col = "text"
        elif "content" in df.columns:
            text_col = "content"
        else:
            text_col = df.columns[1] if len(df.columns) > 1 else title_col

        # Combiner texte
        df["statement"] = (
            df[title_col].fillna("").astype(str)
            + " "
            + df[text_col].fillna("").astype(str)
        )

        texts.extend(df["statement"].tolist())
        labels.extend(df["label"].tolist())

    print(
        f" Loaded {len(texts):,} articles "
        f"({sum(l==0 for l in labels):,} fake, "
        f"{sum(l==1 for l in labels):,} real)"
    )

else:
    print("\n No CSV files found — using built-in demo dataset...")
    print(" (Place datasets in backend/datasets/)")
    _generate_demo_data(texts, labels)

    # Preprocessing
    print("\n Preprocessing text...")
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from preprocessing.clean_text import clean_text

    cleaned = []
    for i, t in enumerate(texts):
        cleaned.append(clean_text(str(t)))
        if (i + 1) % 1000 == 0:
            print(f"   {i+1:,}/{len(texts):,} done...")

    # Vectorization
    print("\n Fitting TF-IDF vectorizers...")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from scipy.sparse import hstack

    word_tfidf = TfidfVectorizer(max_features=10_000, ngram_range=(1, 2), sublinear_tf=True, min_df=2)
    char_tfidf = TfidfVectorizer(analyzer="char_wb", max_features=5_000, ngram_range=(3, 5), sublinear_tf=True, min_df=2)

   
    
def train_and_save():

    print("\n Training Logistic Regression...")

    import numpy as np
    import pickle
    from sklearn.feature_extraction.text import TfidfVectorizer
    from scipy.sparse import hstack
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, f1_score

    # =========================
    # VECTORISATION
    # =========================
    print("\n Fitting TF-IDF vectorizers...")

    word_tfidf = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=2
    )

    char_tfidf = TfidfVectorizer(
        analyzer="char_wb",
        max_features=5000,
        ngram_range=(3, 5),
        sublinear_tf=True,
        min_df=2
    )

    X_word = word_tfidf.fit_transform(cleaned)
    X_char = char_tfidf.fit_transform(cleaned)

    X = hstack([X_word, X_char])
    y = np.array(labels)

    print(f" Feature matrix: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        C=1.0,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("\n Results on test set:")
    print(f"   Accuracy : {acc:.4f}")
    print(f"   F1 Score : {f1:.4f}")

    # Save models
    with open(MODEL_DIR / "fake_news_model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open(MODEL_DIR / "vectorizer_word.pkl", "wb") as f:
        pickle.dump(word_tfidf, f)

    with open(MODEL_DIR / "vectorizer_char.pkl", "wb") as f:
        pickle.dump(char_tfidf, f)

    print(f"\n Model saved to: {MODEL_DIR}")
    print("═" * 55)

    return acc


if __name__ == "__main__":
    train_and_save()