import streamlit as st

st.set_page_config(page_title="Simulateur", page_icon="⚡")

st.title("⚡ Simulateur What-If")

# Vérifier si des données existent déjà
if 'user_data' not in st.session_state:
    st.warning("⚠️ Aucune donnée trouvée. Veuillez d'abord remplir le formulaire dans la page 'Eligibility'.")
else:
    # Récupérer les données de la session
    data = st.session_state['user_data']
    current_result = st.session_state.get('last_result', 'Inconnu')
    
    st.info(f"Votre résultat actuel est : **{current_result}**")
    st.markdown("Ajustez les curseurs pour voir l'impact en temps réel.")

    col1, col2 = st.columns(2)
    
    with col1:
        # On initialise le slider avec la valeur que l'utilisateur avait entrée
        new_income = st.slider("Nouveau Revenu Annuel", 10000, 150000, int(data['annual_income']))
        
    with col2:
        new_debt = st.slider("Nouvelle Dette", 0, 10000, int(data['outstanding_debt']))

    # Logique Mock dynamique
    if new_income > 40000 and new_debt < 2000:
        st.success("👉 Avec ces valeurs, votre score deviendrait : **Good**")
    else:
        st.warning("👉 Avec ces valeurs, votre score resterait : **Standard/Risqué**")