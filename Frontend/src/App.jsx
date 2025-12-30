import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
import Home from "./Home.jsx";
import Eligibility from "./Eligibility.jsx";
import Simulator from "./Simulator.jsx";
import { DataProvider } from "./DataContext.jsx";

// Petit composant pour les liens de navigation (pour gérer l'effet "actif")
const NavLink = ({ to, icon, label }) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  return (
    <Link
      to={to}
      className={`flex items-center space-x-3 px-4 py-3 rounded-md transition-colors ${
        isActive 
          ? "bg-red-50 text-red-600 font-semibold border-l-4 border-red-500" 
          : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
      }`}
    >
      <span className="text-xl">{icon}</span>
      <span>{label}</span>
    </Link>
  );
};

function App() {
  return (
    <DataProvider>
      <Router>
        <div className="flex min-h-screen bg-streamlit-bg font-sans">
          
          {/* Sidebar Fixe */}
          <nav className="w-72 bg-white border-r border-gray-200 h-screen fixed top-0 left-0 p-6 flex flex-col shadow-sm z-10">
            <div className="mb-10">
              <h1 className="text-2xl font-bold text-gray-800 tracking-tight">Credit Score AI</h1>
              <span className="text-xs text-gray-400 uppercase tracking-wider font-semibold">Dashboard MLOps</span>
            </div>
            
            <div className="space-y-2 flex-1">
              <NavLink to="/" icon="🏠" label="Home" />
              <NavLink to="/eligibility" icon="✅" label="Eligibility Check" />
              <NavLink to="/simulator" icon="⚡" label="What-If Simulator" />
            </div>

            <div className="mt-auto pt-6 border-t border-gray-100">
              <p className="text-xs text-gray-400">© 2025 Projet MLOps</p>
            </div>
          </nav>

          {/* Zone de Contenu Principale */}
          <main className="flex-1 ml-72 p-10">
            <div className="max-w-5xl mx-auto bg-white p-8 rounded-xl shadow-sm border border-gray-100 min-h-[80vh]">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/eligibility" element={<Eligibility />} />
                <Route path="/simulator" element={<Simulator />} />
              </Routes>
            </div>
          </main>
          
        </div>
      </Router>
    </DataProvider>
  );
}

export default App;

