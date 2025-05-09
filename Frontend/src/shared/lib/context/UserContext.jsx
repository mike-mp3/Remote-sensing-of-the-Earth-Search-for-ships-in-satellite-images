import { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [userEmail, setUserEmail] = useState("example@mail.ru");

    const updateUserEmail = (email) => {
        setUserEmail(email);
    };

    return (
        <UserContext.Provider value={{ userEmail, updateUserEmail }}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
}; 