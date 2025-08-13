// Language configuration for FarmMate Agricultural AI
// Centralized language support for status messages

const SUPPORTED_LANGUAGES = {
    'en': {
        name: 'English',
        nativeName: 'English',
        direction: 'ltr'
    },
    'hi': {
        name: 'Hindi',
        nativeName: 'हिंदी',
        direction: 'ltr'
    },
    'mr': {
        name: 'Marathi',
        nativeName: 'मराठी',
        direction: 'ltr'
    },
    'gu': {
        name: 'Gujarati',
        nativeName: 'ગુજરાતી',
        direction: 'ltr'
    },
    'pa': {
        name: 'Punjabi',
        nativeName: 'ਪੰਜਾਬੀ',
        direction: 'ltr'
    }
}

const STATUS_MESSAGES = {
    messageReceived: {
        'en': 'Your question has been received. Please wait...',
        'hi': 'आपका प्रश्न प्राप्त हुआ है। कृपया प्रतीक्षा करें...',
        'mr': 'तुमचा प्रश्न प्राप्त झाला आहे. कृपया प्रतीक्षा करा...',
        'gu': 'તમારો પ્રશ્ન પ્રાપ્ત થયો છે. કૃપા કરીને રાહ જુઓ...',
        'pa': 'ਤੁਹਾਡਾ ਸਵਾਲ ਮਿਲ ਗਿਆ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਇੰਤਜ਼ਾਰ ਕਰੋ...'
    },
    analyzingQuery: {
        'en': 'Analyzing your question...',
        'hi': 'आपके प्रश्न का विश्लेषण हो रहा है...',
        'mr': 'तुमच्या प्रश्नाचे विश्लेषण होत आहे...',
        'gu': 'તમારા પ્રશ્નનું વિશ્લેષણ થઈ રહ્યું છે...',
        'pa': 'ਤੁਹਾਡੇ ਸਵਾਲ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਹੋ ਰਿਹਾ ਹੈ...'
    },
    generatingResponse: {
        'en': 'Generating response...',
        'hi': 'उत्तर तैयार किया जा रहा है...',
        'mr': 'उत्तर तयार केले जात आहे...',
        'gu': 'જવાબ તૈયાર કરવામાં આવી રહ્યો છે...',
        'pa': 'ਜਵਾਬ ਤਿਆਰ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...'
    },
    processing: {
        'en': 'Processing...',
        'hi': 'प्रक्रिया जारी है...',
        'mr': 'प्रक्रिया सुरू आहे...',
        'gu': 'પ્રક્રિયા ચાલુ છે...',
        'pa': 'ਪ੍ਰਕਿਰਿਆ ਜਾਰੀ ਹੈ...'
    }
}

const ERROR_MESSAGES = {
    processingError: {
        'en': 'Processing error occurred. Please try again.',
        'hi': 'प्रोसेसिंग में त्रुटि हुई। कृपया पुनः प्रयास करें।',
        'mr': 'प्रक्रिया त्रुटी आली आहे. कृपया पुन्हा प्रयत्न करा.',
        'gu': 'પ્રક્રિયામાં ભૂલ આવી છે. કૃપા કરીને ફરીથી પ્રયાસ કરો.',
        'pa': 'ਪ੍ਰਕਿਰਿਆ ਵਿੱਚ ਗਲਤੀ ਹੋਈ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।'
    },
    connectionError: {
        'en': 'Failed to connect to AI server.',
        'hi': 'AI सर्वर से कनेक्शन में विफलता।',
        'mr': 'AI सर्व्हरशी कनेक्शन अयशस्वी.',
        'gu': 'AI સર્વર સાથે જોડાણ અસફળ.',
        'pa': 'AI ਸਰਵਰ ਨਾਲ ਕਨੈਕਸ਼ਨ ਅਸਫਲ।'
    },
    responseError: {
        'en': 'Failed to process AI response.',
        'hi': 'AI उत्तर संसाधित करने में विफलता।',
        'mr': 'AI प्रतिसाद प्रक्रिया अयशस्वी.',
        'gu': 'AI પ્રતિસાદ પ્રક્રિયા અસફળ.',
        'pa': 'AI ਜਵਾਬ ਪ੍ਰਕਿਰਿਆ ਅਸਫਲ।'
    },
    serverError: {
        'en': 'Internal server error.',
        'hi': 'आंतरिक सर्वर त्रुटि।',
        'mr': 'अंतर्गत सर्व्हर त्रुटी.',
        'gu': 'આંતરિક સર્વર ભૂલ.',
        'pa': 'ਅੰਦਰੂਨੀ ਸਰਵਰ ਗਲਤੀ।'
    }
}

const LABELS = {
    explanation: {
        'en': 'Explanation',
        'hi': 'विस्तार',
        'mr': 'तपशील',
        'gu': 'વિગત',
        'pa': 'ਵੇਰਵਾ'
    },
    location: {
        'en': 'Location',
        'hi': 'स्थान',
        'mr': 'ठिकाण',
        'gu': 'સ્થાન',
        'pa': 'ਸਥਾਨ'
    },
    topic: {
        'en': 'Topic',
        'hi': 'विषय',
        'mr': 'विषय',
        'gu': 'વિષય',
        'pa': 'ਵਿਸ਼ਾ'
    }
}

function isLanguageSupported(langCode) {
    return SUPPORTED_LANGUAGES.hasOwnProperty(langCode)
}

function getStatusMessage(messageType, langCode, stage = null) {
    const defaultLang = 'en'
    
    if (!isLanguageSupported(langCode)) {
        langCode = defaultLang
    }
    
    if (messageType === 'status_update' && stage) {
        const stageMessages = STATUS_MESSAGES[stage]
        return stageMessages ? (stageMessages[langCode] || stageMessages[defaultLang]) : STATUS_MESSAGES.processing[langCode]
    }
    
    const messages = STATUS_MESSAGES[messageType]
    return messages ? (messages[langCode] || messages[defaultLang]) : 'Processing...'
}

function getLabel(labelType, langCode) {
    const defaultLang = 'en'
    
    if (!isLanguageSupported(langCode)) {
        langCode = defaultLang
    }
    
    const labels = LABELS[labelType]
    return labels ? (labels[langCode] || labels[defaultLang]) : labelType
}

function getErrorMessage(errorType, langCode) {
    const defaultLang = 'en'
    
    if (!isLanguageSupported(langCode)) {
        langCode = defaultLang
    }
    
    const errorMessages = ERROR_MESSAGES[errorType]
    return errorMessages ? (errorMessages[langCode] || errorMessages[defaultLang]) : ERROR_MESSAGES.processingError[langCode]
}

function getSupportedLanguages() {
    return SUPPORTED_LANGUAGES
}

module.exports = {
    SUPPORTED_LANGUAGES,
    STATUS_MESSAGES,
    ERROR_MESSAGES,
    LABELS,
    isLanguageSupported,
    getStatusMessage,
    getLabel,
    getErrorMessage,
    getSupportedLanguages
}
