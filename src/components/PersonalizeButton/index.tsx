import React, { useState } from 'react';
import styles from './styles.module.css';

interface PersonalizeButtonProps {
  chapter: string;
  content: string;
  selectedText?: string;
  onPersonalized?: (personalizedContent: string) => void;
}

const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({
  chapter,
  content,
  selectedText,
  onPersonalized
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);

  const handlePersonalize = async () => {
    setIsLoading(true);

    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        alert('Please log in to use personalization features.');
        return;
      }

      const response = await fetch('/api/personalization/adapt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          chapter,
          original_content: content,
          selected_text: selectedText
        })
      });

      if (response.ok) {
        const data = await response.json();
        setIsPersonalized(true);
        onPersonalized?.(data.personalized_content);

        // Show success message
        alert('Content personalized successfully! The page will update with your customized content.');
      } else if (response.status === 401) {
        alert('Please log in to use personalization features.');
      } else {
        alert('Personalization failed. Please try again.');
      }
    } catch (error) {
      console.error('Personalization error:', error);
      alert('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      className={`${styles.personalizeButton} ${isPersonalized ? styles.personalized : ''}`}
      onClick={handlePersonalize}
      disabled={isLoading}
      title="Personalize content based on your profile"
    >
      {isLoading ? (
        <>
          <div className={styles.spinner}></div>
          Personalizing...
        </>
      ) : isPersonalized ? (
        <>
          ✨ Personalized
        </>
      ) : (
        <>
          🎯 Personalize
        </>
      )}
    </button>
  );
};

export default PersonalizeButton;
