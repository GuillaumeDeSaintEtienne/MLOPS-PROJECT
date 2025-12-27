import React from 'react';

const Home = () => {
    return (
        <div className="p-8 max-w-4xl mx-auto">
            <h1 className="text-4xl font-bold mb-4">🏦 Projet MLOps : Credit Score</h1>
            <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h3 className="text-xl font-semibold mb-2">Bienvenue sur notre plateforme de prédiction</h3>
                <p className="text-gray-600 mb-4">Ce projet utilise le Machine Learning pour évaluer l'éligibilité aux prêts bancaires.</p>
                
                <div className="space-y-2">
                    <p><strong>1. ✅ Eligibility Check</strong> : Remplissez votre profil pour obtenir une décision immédiate.</p>
                    <p><strong>2. ⚡ What-If Simulator</strong> : Simulez différents scénarios pour voir comment améliorer votre score.</p>
                </div>
                <hr className="my-6" />
                <p className="italic text-sm text-gray-400">Réalisé par : Masao, Guillaume, Mael, Emilien</p>
            </div>
        </div>
    );
};

export default Home;