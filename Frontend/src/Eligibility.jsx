import React, { useState, useEffect } from 'react';
import { useData } from './DataContext.jsx';

// 1. IMPROVED COMPONENT: Accepts ...props to allow things like min="0"
const InputField = ({ label, value, onChange, type = "number", prefix, ...props }) => (
    <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 mb-2">{label}</label>
        <div className="relative rounded-md shadow-sm">
            {prefix && (
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                    <span className="text-gray-500 sm:text-sm">{prefix}</span>
                </div>
            )}
            <input
                type={type}
                className={`block w-full rounded-md border-0 py-2.5 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-red-500 sm:text-sm sm:leading-6 ${prefix ? 'pl-8' : 'pl-3'}`}
                value={value}
                onChange={onChange}
                {...props} // Allows passing min, max, placeholder, etc.
            />
        </div>
    </div>
);

const Eligibility = () => {
    // 2. GET USERDATA: We pull existing data from context
    const { setUserData, setResult, result, userData } = useData();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // 3. PERSISTENCE: Initialize form with existing userData if available, otherwise defaults
    const [form, setForm] = useState(userData || {
        Annual_Income: 50000,
        Monthly_Inhand_Salary: 4000,
        Outstanding_Debt: 1000,
        Credit_History_Age: 5,     
        Num_Bank_Accounts: 2,
        Num_Credit_Cards: 3
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        // Prepare Payload
        const payload = {
            Annual_Income: parseFloat(form.Annual_Income),
            Monthly_Inhand_Salary: parseFloat(form.Monthly_Inhand_Salary),
            Num_Bank_Accounts: parseInt(form.Num_Bank_Accounts),
            Num_Credit_Cards: parseInt(form.Num_Credit_Cards),
            Outstanding_Debt: parseFloat(form.Outstanding_Debt),
            Credit_History_Age: parseFloat(form.Credit_History_Age) * 12 
        };

        try {
            const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const response = await fetch(`${apiUrl}/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error("Erreur serveur lors de la prédiction");
            }

            const data = await response.json();
            
            // Handle Result
            const prediction = data.credit_score; 
            const isGood = prediction === "Good" || prediction === "Standard";
            
            // Save to Context (Global State)
            setUserData(form);
            setResult({ 
                label: prediction, 
                isApproved: isGood 
            });

        } catch (err) {
            console.error(err);
            setError("Impossible de contacter l'IA. Vérifiez que le backend tourne.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="animate-fade-in max-w-5xl mx-auto p-4">
            <div className="border-b pb-4 mb-6">
                <h1 className="text-3xl font-bold text-gray-800">✅ Vérification d'Éligibilité</h1>
                <p className="text-gray-500 mt-2">Remplissez ces 6 critères clés pour une décision IA immédiate.</p>
            </div>

            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Colonne Gauche */}
                <div className="space-y-2">
                    <InputField 
                        label="Revenu Annuel ($)" 
                        value={form.Annual_Income} 
                        prefix="$" 
                        min="0"
                        onChange={(e) => setForm({...form, Annual_Income: e.target.value})} 
                    />
                    <InputField 
                        label="Salaire Mensuel Net ($)" 
                        value={form.Monthly_Inhand_Salary} 
                        prefix="$" 
                        min="0"
                        onChange={(e) => setForm({...form, Monthly_Inhand_Salary: e.target.value})} 
                    />
                    <InputField 
                        label="Âge Historique Crédit (Années)" 
                        value={form.Credit_History_Age} 
                        min="0"
                        onChange={(e) => setForm({...form, Credit_History_Age: e.target.value})} 
                    />
                </div>

                {/* Colonne Droite */}
                <div className="space-y-2">
                    <InputField 
                        label="Dette Totale ($)" 
                        value={form.Outstanding_Debt} 
                        prefix="$" 
                        min="0"
                        onChange={(e) => setForm({...form, Outstanding_Debt: e.target.value})} 
                    />
                    <InputField 
                        label="Nombre de Cartes de Crédit" 
                        value={form.Num_Credit_Cards} 
                        min="0"
                        onChange={(e) => setForm({...form, Num_Credit_Cards: e.target.value})} 
                    />
                    <InputField 
                        label="Nombre de Comptes Bancaires" 
                        value={form.Num_Bank_Accounts} 
                        min="0"
                        onChange={(e) => setForm({...form, Num_Bank_Accounts: e.target.value})} 
                    />
                    
                    <div className="pt-6">
                        <button 
                            type="submit" 
                            disabled={loading}
                            className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white transition-all 
                            ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500'}`}
                        >
                            {loading ? (
                                <span className="flex items-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Analyse en cours...
                                </span>
                            ) : "Lancer la prédiction IA"}
                        </button>
                    </div>
                </div>
            </form>

            {/* Zone d'Erreur */}
            {error && (
                <div className="mt-4 p-4 text-red-700 bg-red-100 rounded-md border border-red-400 animate-pulse">
                    ⚠️ {error}
                </div>
            )}

            {/* Zone de Résultat */}
            {result.label && !loading && (
                <div className={`mt-8 p-6 rounded-lg border-l-4 shadow-sm animate-slide-up ${
                    result.isApproved ? 'bg-green-50 border-green-500 text-green-800' : 'bg-red-50 border-red-500 text-red-800'
                }`}>
                    <h3 className="text-xl font-bold flex items-center mb-2">
                        {result.isApproved ? '🎉 Félicitations' : '⚠️ Risque Détecté'}
                    </h3>
                    
                    <div className="flex items-center space-x-4">
                        <div className="text-lg">
                             Score de Crédit Estimé :
                        </div>
                        <div className={`px-4 py-1 rounded-full text-white font-bold text-sm tracking-wider uppercase shadow-sm ${
                            result.label === 'Good' ? 'bg-green-600' : 
                            result.label === 'Standard' ? 'bg-blue-600' : 'bg-red-600'
                        }`}>
                            {result.label}
                        </div>
                    </div>

                    {!result.isApproved && (
                        <p className="mt-4 text-sm text-blue-700 hover:text-blue-900 underline cursor-pointer transition-colors">
                            💡 Conseil : Allez sur le Simulateur pour voir comment améliorer votre score.
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Eligibility;