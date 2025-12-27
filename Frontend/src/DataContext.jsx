import React, { createContext, useState, useContext } from 'react';

const DataContext = createContext();

export const DataProvider = ({ children }) => {
    const [userData, setUserData] = useState(null);
    const [result, setResult] = useState({ label: '', isApproved: false });

    return (
        <DataContext.Provider value={{ userData, setUserData, result, setResult }}>
            {children}
        </DataContext.Provider>
    );
};

export const useData = () => useContext(DataContext);