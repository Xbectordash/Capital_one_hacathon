// Language Selector Component for FarmMate Agricultural AI
import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import './LanguageSelector.css';

const LanguageSelector = ({ disabled = false, className = '' }) => {
  const { currentLanguage, changeLanguage, supportedLanguages, t } = useLanguage();

  const handleLanguageChange = (event) => {
    const newLanguage = event.target.value;
    changeLanguage(newLanguage);
  };

  return (
    <div className={`language-selector ${className}`}>
      <label htmlFor="language-select" className="language-label">
        {t('languageLabel')}
      </label>
      <select
        id="language-select"
        value={currentLanguage}
        onChange={handleLanguageChange}
        disabled={disabled}
        className="language-dropdown"
        aria-label={t('languageLabel')}
      >
        {supportedLanguages.map((language) => (
          <option key={language.code} value={language.code}>
            {language.nativeName}
          </option>
        ))}
      </select>
    </div>
  );
};

export default LanguageSelector;
