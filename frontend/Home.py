import streamlit as st

st.set_page_config(
    page_title="Credit Score AI",
    page_icon="🏦",
)

st.title("🏦 Projet MLOps : Credit Score")

st.markdown("""
### Bienvenue sur notre plateforme de prédiction

Ce projet utilise le Machine Learning pour évaluer l'éligibilité aux prêts bancaires.

**Utilisez la barre latérale à gauche pour naviguer :**

1. **✅ Eligibility Check** : Remplissez votre profil pour obtenir une décision immédiate.
2. **⚡ What-If Simulator** : Simulez différents scénarios pour voir comment améliorer votre score.

---
*Réalisé par : Masao, Guillaume, Mael, Emilien*
""")