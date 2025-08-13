// Language Context for FarmMate Agricultural AI
import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  getTranslation, 
  loadLanguagePreference, 
  saveLanguagePreference,
  supportedLanguages,
  defaultLanguage 
} from '../locales';

// Create Language Context
const LanguageContext = createContext();

// Custom hook to use language context
export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Language Provider Component
export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(defaultLanguage);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize language on component mount
  useEffect(() => {
    const initializeLanguage = async () => {
      try {
        const savedLanguage = loadLanguagePreference();
        setCurrentLanguage(savedLanguage);
      } catch (error) {
        console.error('Error initializing language:', error);
        setCurrentLanguage(defaultLanguage);
      } finally {
        setIsLoading(false);
      }
    };

    initializeLanguage();
  }, []);

  // Change language function
  const changeLanguage = (languageCode) => {
    if (supportedLanguages.find(lang => lang.code === languageCode)) {
      setCurrentLanguage(languageCode);
      saveLanguagePreference(languageCode);
    } else {
      console.warn(`Unsupported language: ${languageCode}`);
    }
  };

  // Translation function with current language
  const t = (key, fallback) => {
    return getTranslation(currentLanguage, key, fallback);
  };

  // Get current language info
  const getCurrentLanguageInfo = () => {
    return supportedLanguages.find(lang => lang.code === currentLanguage) || 
           supportedLanguages.find(lang => lang.code === defaultLanguage);
  };

  // Check if RTL language
  const isRTL = () => {
    const langInfo = getCurrentLanguageInfo();
    return langInfo ? langInfo.rtl : false;
  };

  const value = {
    currentLanguage,
    changeLanguage,
    t,
    supportedLanguages,
    getCurrentLanguageInfo,
    isRTL,
    isLoading
  };

  if (isLoading) {
    return (
      <div className="language-loading">
        <div className="loading-spinner">🔄</div>
        <div>Loading language preferences...</div>
      </div>
    );
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};
