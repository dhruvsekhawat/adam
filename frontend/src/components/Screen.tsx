import React from 'react';

interface ScreenProps {
  children: React.ReactNode;
}

const Screen: React.FC<ScreenProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-white">
      {children}
    </div>
  );
};

export default Screen; 