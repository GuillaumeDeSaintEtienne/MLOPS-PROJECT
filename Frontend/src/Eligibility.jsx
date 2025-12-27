import React, { useState } from 'react';
import { useData } from './DataContext.jsx';

const InputField = ({ label, value, onChange, type = "number", prefix }) => (
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
            />
        </div>
    </div>
);

const Eligibility = () => {
    const { setUserData, setResult, result } = useData();
    const [loading, setLoading] = useState(false);
    const [form, setForm] = useState({
        annual_income: 50000,
        monthly_salary: 4000,
        credit_age: 5.0,
        outstanding_debt: 1000,
        num_bank_accounts: 2
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        setTimeout(() => {
            const isGood = form.annual_income > 40000 && form.outstanding_debt < 2000;
            const status = isGood ? "Good (Approuvé)" : "Standard (Risqué)";
            setUserData(form);
            setResult({ label: status, isApproved: isGood });
            setLoading(false);
        }, 1000);
    };

    return (
        <div className="animate-fade-in">
            <div className="border-b pb-4 mb-6">
                <h1 className="text-3xl font-bold text-gray-800">✅ Vérification d'Éligibilité</h1>
                <p className="text-gray-500 mt-2">Remplissez le formulaire pour obtenir une décision IA immédiate.</p>
            </div>

            <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Colonne Gauche */}
                <div className="space-y-2">
                    <InputField label="Revenu Annuel ($)" value={form.annual_income} prefix="$" onChange={(e) => setForm({...form, annual_income: +e.target.value})} />
                    <InputField label="Salaire Mensuel ($)" value={form.monthly_salary} prefix="$" onChange={(e) => setForm({...form, monthly_salary: +e.target.value})} />
                    <InputField label="Âge Historique Crédit (Années)" value={form.credit_age} onChange={(e) => setForm({...form, credit_age: +e.target.value})} />
                </div>

                {/* Colonne Droite */}
                <div className="space-y-2">
                    <InputField label="Dette Totale ($)" value={form.outstanding_debt} prefix="$" onChange={(e) => setForm({...form, outstanding_debt: +e.target.value})} />
                    <InputField label="Nombre de comptes bancaires" value={form.num_bank_accounts} onChange={(e) => setForm({...form, num_bank_accounts: +e.target.value})} />
                    
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
                            ) : "Lancer la prédiction"}
                        </button>
                    </div>
                </div>
            </form>

            {/* Zone de Résultat */}
            {result.label && !loading && (
                <div className={`mt-8 p-6 rounded-lg border-l-4 shadow-sm animate-slide-up ${
                    result.isApproved ? 'bg-green-50 border-green-500 text-green-800' : 'bg-red-50 border-red-500 text-red-800'
                }`}>
                    <h3 className="text-lg font-bold flex items-center">
                        {result.isApproved ? '🎉 Félicitations' : '⚠️ Attention'}
                    </h3>
                    <p className="mt-2 text-lg">
                        Résultat du modèle : <strong className="text-2xl ml-2">{result.label}</strong>
                    </p>
                    {!result.isApproved && (
                        <p className="mt-4 text-sm text-blue-700 underline cursor-pointer">
                            Conseil : Allez sur le Simulateur pour voir comment améliorer ce score.
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Eligibility;