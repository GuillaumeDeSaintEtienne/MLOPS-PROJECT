import React, { useState, useEffect } from 'react';
import { useData } from './DataContext';

const Simulator = () => {
    const { userData, result } = useData();
    
    // 1. Initialize with userData, but ensure keys match what Backend expects
    // We use "Annual_Income" (PascalCase) because that's what your API defined.
    const [simData, setSimData] = useState(null);
    const [simulatedResult, setSimulatedResult] = useState(null);
    const [loading, setLoading] = useState(false);

    // Initialize state when userData loads
    useEffect(() => {
        if (userData) {
            setSimData(userData);
            setSimulatedResult(result?.label || "Unknown");
        }
    }, [userData, result]);

    // 2. DEBOUNCED API CALL
    // This effect runs every time 'simData' changes, but waits 600ms before calling API
    useEffect(() => {
        if (!simData) return;

        setLoading(true);
        const timer = setTimeout(async () => {
            await fetchSimulation();
        }, 600); // Wait 600ms after user stops sliding

        return () => clearTimeout(timer); // Cleanup (Cancel previous timer if user moves again)
    }, [simData]);

    const fetchSimulation = async () => {
        try {
            // Reconstruct the Payload exactly like in Eligibility.jsx
            // Use values from simData (the sliders)
            const payload = {
                Annual_Income: parseFloat(simData.Annual_Income),
                Monthly_Inhand_Salary: parseFloat(simData.Monthly_Inhand_Salary),
                Num_Bank_Accounts: parseInt(simData.Num_Bank_Accounts),
                Num_Credit_Cards: parseInt(simData.Num_Credit_Cards),
                Outstanding_Debt: parseFloat(simData.Outstanding_Debt),
                Credit_History_Age: parseFloat(simData.Credit_History_Age) * 12 
            };

            const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
            const response = await fetch(`${apiUrl}/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();
            setSimulatedResult(data.credit_score); // Update the result!
        } catch (error) {
            console.error("Simulation failed:", error);
        } finally {
            setLoading(false);
        }
    };

    if (!simData) {
        return <div className="p-8 text-orange-600 font-bold">⚠️ Aucune donnée. Veuillez remplir le formulaire d'abord.</div>;
    }

    // Helper to determine color based on score text
    const getScoreColor = (score) => {
        if (score === "Good") return "text-green-600 bg-green-50 border-green-200";
        if (score === "Standard") return "text-blue-600 bg-blue-50 border-blue-200";
        return "text-red-600 bg-red-50 border-red-200";
    };

    return (
        <div className="p-8 max-w-5xl mx-auto animate-fade-in">
            <h1 className="text-3xl font-bold mb-2">⚡ Simulateur Interactif</h1>
            <p className="text-gray-500 mb-8">Bougez les curseurs pour voir comment l'IA réagit en temps réel.</p>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* --- CONTROLS SECTION (Left) --- */}
                <div className="lg:col-span-2 space-y-8 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                    
                    {/* Slider: Income */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="font-semibold text-gray-700">Revenu Annuel</label>
                            <span className="font-mono text-blue-600 bg-blue-50 px-2 rounded">${simData.Annual_Income}</span>
                        </div>
                        <input 
                            type="range" min="10000" max="150000" step="1000"
                            className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                            value={simData.Annual_Income} 
                            onChange={(e) => setSimData({...simData, Annual_Income: e.target.value})} 
                        />
                        <div className="flex justify-between text-xs text-gray-400 mt-1">
                            <span>$10k</span>
                            <span>$150k</span>
                        </div>
                    </div>

                    {/* Slider: Debt */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="font-semibold text-gray-700">Dette Totale</label>
                            <span className="font-mono text-red-600 bg-red-50 px-2 rounded">${simData.Outstanding_Debt}</span>
                        </div>
                        <input 
                            type="range" min="0" max="5000" step="100"
                            className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-red-500"
                            value={simData.Outstanding_Debt} 
                            onChange={(e) => setSimData({...simData, Outstanding_Debt: e.target.value})} 
                        />
                    </div>

                     {/* Slider: Credit Cards */}
                     <div>
                        <div className="flex justify-between mb-2">
                            <label className="font-semibold text-gray-700">Cartes de Crédit</label>
                            <span className="font-mono text-gray-800 bg-gray-100 px-2 rounded">{simData.Num_Credit_Cards}</span>
                        </div>
                        <input 
                            type="range" min="0" max="12" step="1"
                            className="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-gray-600"
                            value={simData.Num_Credit_Cards} 
                            onChange={(e) => setSimData({...simData, Num_Credit_Cards: e.target.value})} 
                        />
                    </div>
                </div>

                {/* --- RESULT SECTION (Right / Floating) --- */}
                <div className="lg:col-span-1">
                    <div className="sticky top-8 bg-white p-6 rounded-xl shadow-lg border border-gray-200 text-center">
                        <h2 className="text-gray-500 font-medium uppercase tracking-wider text-sm mb-4">Prédiction IA</h2>
                        
                        {loading ? (
                            <div className="py-8 animate-pulse">
                                <div className="h-4 bg-gray-200 rounded w-3/4 mx-auto mb-2"></div>
                                <div className="h-8 bg-gray-300 rounded w-1/2 mx-auto"></div>
                                <p className="text-sm text-gray-400 mt-2">Calcul en cours...</p>
                            </div>
                        ) : (
                            <div className={`py-6 rounded-lg border-2 ${getScoreColor(simulatedResult)} transition-all duration-300`}>
                                <div className="text-4xl font-extrabold mb-1">
                                    {simulatedResult}
                                </div>
                                <p className="text-sm font-medium opacity-80">Score Estimé</p>
                            </div>
                        )}

                        <div className="mt-6 pt-6 border-t border-gray-100">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-500">Score Original:</span>
                                <span className="font-semibold text-gray-700">{result?.label || "N/A"}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Simulator;