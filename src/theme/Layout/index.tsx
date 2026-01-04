import React from 'react';
import Layout from '@theme/Layout';
import AuthButtons from '../../components/AuthButtons';
import ChatWidget from '../../components/ChatWidget';

interface CustomLayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  image?: string;
  keywords?: string[];
  permalink?: string;
  wrapperClassName?: string;
  pageClassName?: string;
  searchMetadatas?: {
    version?: string;
    tag?: string;
  };
}

const CustomLayout: React.FC<CustomLayoutProps> = (props) => {
  return (
    <Layout {...props}>
      {/* Auth Buttons in top-right corner */}
      <div style={{
        position: 'fixed',
        top: '1rem',
        right: '1rem',
        zIndex: 1000
      }}>
        <AuthButtons />
      </div>

      {/* Chat Widget floating on all pages */}
      <ChatWidget />

      {props.children}
    </Layout>
  );
};

export default CustomLayout;
