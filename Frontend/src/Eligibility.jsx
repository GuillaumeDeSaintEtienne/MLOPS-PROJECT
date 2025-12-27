import React, { useState } from 'react';
import { useData } from './DataContext';

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

        // Simulation delay
        setTimeout(() => {
            const isGood = form.annual_income > 40000 && form.outstanding_debt < 2000;
            const status = isGood ? "Good (Approuvé)" : "Standard (Risqué)";
            
            setUserData(form);
            setResult({ label: status, isApproved: isGood });
            setLoading(false);
        }, 1000);
    };

    return (
        <div className="p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-2">✅ Vérification d'Éligibilité</h1>
            <p className="text-gray-500 mb-6">Remplissez le formulaire ci-dessous pour lancer l'analyse.</p>

            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-6 bg-gray-50 p-6 rounded-xl border">
                <div>
                    <label className="block text-sm font-medium">Revenu Annuel ($)</label>
                    <input type="number" className="w-full p-2 border rounded" value={form.annual_income} 
                        onChange={(e) => setForm({...form, annual_income: +e.target.value})} />
                    
                    <label className="block mt-4 text-sm font-medium">Salaire Mensuel ($)</label>
                    <input type="number" className="w-full p-2 border rounded" value={form.monthly_salary} 
                        onChange={(e) => setForm({...form, monthly_salary: +e.target.value})} />
                </div>
                <div>
                    <label className="block text-sm font-medium">Dette Totale ($)</label>
                    <input type="number" className="w-full p-2 border rounded" value={form.outstanding_debt} 
                        onChange={(e) => setForm({...form, outstanding_debt: +e.target.value})} />
                    
                    <label className="block mt-4 text-sm font-medium">Nombre de comptes</label>
                    <input type="number" className="w-full p-2 border rounded" value={form.num_bank_accounts} 
                        onChange={(e) => setForm({...form, num_bank_accounts: +e.target.value})} />
                </div>
                <button type="submit" className="col-span-2 bg-red-500 text-white p-2 rounded hover:bg-red-600 transition">
                    {loading ? "Chargement..." : "Lancer la prédiction"}
                </button>
            </form>

            {result.label && !loading && (
                <div className={`mt-6 p-4 rounded border ${result.isApproved ? 'bg-green-100 border-green-500 text-green-700' : 'bg-red-100 border-red-500 text-red-700'}`}>
                    Résultat : <strong>{result.label}</strong>
                    {!result.isApproved && <p className="text-sm mt-2 text-blue-600">Allez sur la page 'Simulator' pour voir comment améliorer ce score.</p>}
                </div>
            )}
        </div>
    );
};

export default Eligibility;