import React, { useState } from 'react';
import styles from './styles.module.css';

interface TranslateButtonProps {
  content: string;
  selectedText?: string;
  onTranslated?: (translatedContent: string) => void;
}

const TranslateButton: React.FC<TranslateButtonProps> = ({
  content,
  selectedText,
  onTranslated
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [translationMode, setTranslationMode] = useState<'docusaurus' | 'api'>('api');
  const [showOptions, setShowOptions] = useState(false);

  const handleTranslate = async (mode: 'docusaurus' | 'api') => {
    setIsLoading(true);
    setShowOptions(false);

    try {
      if (mode === 'docusaurus') {
        // For Docusaurus i18n, we'd redirect to Urdu locale
        // This is a simplified implementation
        const currentUrl = window.location.pathname;
        const urduUrl = `/ur${currentUrl}`;
        window.location.href = urduUrl;
        return;
      }

      // API translation
      const response = await fetch('/api/translation/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: selectedText || content,
          source_lang: 'en',
          target_lang: 'ur'
        })
      });

      if (response.ok) {
        const data = await response.json();
        onTranslated?.(data.translated_text);

        // Show translated text in a modal or replace content
        alert(`Translation:\n\n${data.translated_text}`);
      } else {
        alert('Translation failed. Please try again.');
      }
    } catch (error) {
      console.error('Translation error:', error);
      alert('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.translateContainer}>
      <button
        className={styles.translateButton}
        onClick={() => setShowOptions(!showOptions)}
        disabled={isLoading}
        title="Translate content to Urdu"
      >
        {isLoading ? (
          <>
            <div className={styles.spinner}></div>
            Translating...
          </>
        ) : (
          <>
            🌍 اردو
          </>
        )}
      </button>

      {showOptions && (
        <div className={styles.optionsMenu}>
          <button
            className={styles.optionButton}
            onClick={() => handleTranslate('docusaurus')}
            title="Use Docusaurus i18n (full page)"
          >
            📄 Full Page (i18n)
          </button>
          <button
            className={styles.optionButton}
            onClick={() => handleTranslate('api')}
            title="Translate selected text or current section"
          >
            📝 {selectedText ? 'Selected Text' : 'Current Section'} (API)
          </button>
        </div>
      )}
    </div>
  );
};

export default TranslateButton;
