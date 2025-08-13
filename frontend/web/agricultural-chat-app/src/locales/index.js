// Localization configuration for FarmMate Agricultural AI
import { en } from './en';
import { hi } from './hi';
import { mr } from './mr';
import { pa } from './pa';
import { gu } from './gu';

// Available translations
export const translations = {
  en,
  hi,
  mr,
  pa,
  gu
};

// Supported languages with metadata
export const supportedLanguages = [
  { code: 'en', name: 'English', nativeName: 'English', rtl: false },
  { code: 'hi', name: 'Hindi', nativeName: 'हिंदी', rtl: false },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी', rtl: false },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', rtl: false },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી', rtl: false }
];

// Default language
export const defaultLanguage = 'en';

// Get translation for a key with fallback
export const getTranslation = (language, key, fallback = key) => {
  const keys = key.split('.');
  let translation = translations[language] || translations[defaultLanguage];
  
  try {
    for (const k of keys) {
      translation = translation[k];
      if (translation === undefined) {
        throw new Error('Translation not found');
      }
    }
    return translation;
  } catch (error) {
    console.warn(`Translation missing for key: ${key} in language: ${language}`);
    return fallback;
  }
};

// Get browser's preferred language
export const getBrowserLanguage = () => {
  const browserLang = navigator.language || navigator.languages[0];
  const langCode = browserLang.split('-')[0]; // Get language part (e.g., 'hi' from 'hi-IN')
  
  // Return if supported, otherwise default
  return supportedLanguages.find(lang => lang.code === langCode)?.code || defaultLanguage;
};

// Save language preference to localStorage
export const saveLanguagePreference = (language) => {
  try {
    localStorage.setItem('farmmate_language', language);
  } catch (error) {
    console.warn('Could not save language preference:', error);
  }
};

// Load language preference from localStorage
export const loadLanguagePreference = () => {
  try {
    const saved = localStorage.getItem('farmmate_language');
    if (saved && supportedLanguages.find(lang => lang.code === saved)) {
      return saved;
    }
  } catch (error) {
    console.warn('Could not load language preference:', error);
  }
  return getBrowserLanguage();
};
