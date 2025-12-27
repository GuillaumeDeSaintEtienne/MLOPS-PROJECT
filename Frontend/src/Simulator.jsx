import React, { useState, useEffect } from 'react';
import { useData } from './DataContext';

const Simulator = () => {
    const { userData, result } = useData();
    const [simData, setSimData] = useState(userData);

    // Update local simulation data if global data changes
    useEffect(() => {
        if (userData) setSimData(userData);
    }, [userData]);

    if (!userData) {
        return <div className="p-8 text-orange-600 font-bold">⚠️ Aucune donnée trouvée. Veuillez d'abord remplir le formulaire dans 'Eligibility'.</div>;
    }

    const isGood = simData.annual_income > 40000 && simData.outstanding_debt < 2000;

    return (
        <div className="p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">⚡ Simulateur What-If</h1>
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 text-blue-700">
                Votre résultat actuel est : <strong>{result.label}</strong>
            </div>

            <div className="grid grid-cols-2 gap-8 mb-8">
                <div>
                    <label className="block font-medium mb-2">Nouveau Revenu: ${simData.annual_income}</label>
                    <input type="range" min="10000" max="150000" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        value={simData.annual_income} onChange={(e) => setSimData({...simData, annual_income: +e.target.value})} />
                </div>
                <div>
                    <label className="block font-medium mb-2">Nouvelle Dette: ${simData.outstanding_debt}</label>
                    <input type="range" min="0" max="10000" className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        value={simData.outstanding_debt} onChange={(e) => setSimData({...simData, outstanding_debt: +e.target.value})} />
                </div>
            </div>

            {isGood ? (
                <div className="p-4 bg-green-100 border border-green-400 text-green-700 rounded">
                    👉 Avec ces valeurs, votre score deviendrait : <strong>Good</strong>
                </div>
            ) : (
                <div className="p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded">
                    👉 Avec ces valeurs, votre score resterait : <strong>Standard/Risqué</strong>
                </div>
            )}
        </div>
    );
};

export default Simulator;