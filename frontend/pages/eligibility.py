import streamlit as st
import time

st.set_page_config(page_title="Vérification Éligibilité", page_icon="✅")

st.title("✅ Vérification d'Éligibilité")
st.markdown("Remplissez le formulaire ci-dessous pour lancer l'analyse.")

# Formulaire
with st.form("loan_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        annual_income = st.number_input("Revenu Annuel ($)", value=50000, step=1000)
        monthly_salary = st.number_input("Salaire Mensuel ($)", value=4000, step=100)
        credit_age = st.number_input("Âge Crédit (Années)", value=5.0, step=0.1)
        
    with col2:
        outstanding_debt = st.number_input("Dette Totale ($)", value=1000, step=100)
        num_bank_accounts = st.number_input("Nombre de comptes", value=2, step=1)

    submitted = st.form_submit_button("Lancer la prédiction", type="primary")

if submitted:
    # 1. Sauvegarder les données dans la "Session" pour la page 2
    st.session_state['user_data'] = {
        "annual_income": annual_income,
        "outstanding_debt": outstanding_debt,
        "monthly_salary": monthly_salary
    }
    
    with st.spinner('Interrogation du modèle IA...'):
        time.sleep(1) # Simulation
        
        # LOGIQUE MOCK (TEMPORAIRE)
        is_good = (annual_income > 40000 and outstanding_debt < 2000)
        result = "Good (Approuvé)" if is_good else "Standard (Risqué)"
        
        # Sauvegarder le résultat aussi
        st.session_state['last_result'] = result
        st.session_state['is_approved'] = is_good

    # Affichage
    if is_good:
        st.success(f"Résultat : **{result}**")
    else:
        st.error(f"Résultat : **{result}**")
        st.info("Allez sur la page 'Simulator' pour voir comment améliorer ce score.")