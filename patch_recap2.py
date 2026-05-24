from pathlib import Path

p = Path('notebook/Fake_news_net/kenzihamza_puch_TruthGuard_NB2_Modelisation (1).ipynb')
text = p.read_text(encoding='utf-8')
text = text.replace('X_train_emb.shape[1]', '0')
text = text.replace('X_train_stylo.shape[1]', '0')
text = text.replace(
    'print(f"\\n  Train samples            : {X_train_tfidf.shape[0]:,}")\n',
    'print(f"\\n  Train samples            : {X_train_tfidf.shape[0]:,}")\n'
    'print(f"  Test samples             : {X_test_tfidf.shape[0]:,}")\n'
    'print(f"  Labels train             : Fake={(y_train==0).sum():,} | Real={(y_train==1).sum():,}")\n'
)
p.write_text(text, encoding='utf-8')
print('patched')
