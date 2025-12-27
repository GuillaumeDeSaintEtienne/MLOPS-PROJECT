import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from "./Home.jsx";
import Eligibility from "./Eligibility.jsx";
import Simulator from "./Simulator.jsx";
import { DataProvider } from "./DataContext.jsx";

function App() {
  return (
    <DataProvider>
      <Router>
        <div className="flex min-h-screen bg-gray-100">
          {/* Sidebar - Equivalent to Streamlit Sidebar */}
          <nav className="w-64 bg-white shadow-md p-6">
            <h2 className="text-xl font-bold mb-8 text-gray-800">🏦 Credit Score AI</h2>
            <ul className="space-y-4">
              <li>
                <Link title="Home" to="/" className="text-blue-600 hover:underline">🏠 Home</Link>
              </li>
              <li>
                <Link title="Eligibility" to="/eligibility" className="text-blue-600 hover:underline">✅ Eligibility</Link>
              </li>
              <li>
                <Link title="Simulator" to="/simulator" className="text-blue-600 hover:underline">⚡ Simulator</Link>
              </li>
            </ul>
          </nav>

          {/* Main Content Area */}
          <main className="flex-1 p-10">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/eligibility" element={<Eligibility />} />
              <Route path="/simulator" element={<Simulator />} />
            </Routes>
          </main>
        </div>
      </Router>
    </DataProvider>
  );
}

export default App;