import React from 'react';

interface CardProps {
  children: React.ReactNode;
  variant?: 'large' | 'small' | 'demo';
  className?: string;
}

const Card: React.FC<CardProps> = ({ children, variant = 'large', className = '' }) => {
  const baseClasses = {
    large: 'w-[1392px] h-[623px] rounded-[48px]',
    small: 'w-[333px] h-[209px] rounded-[32px]',
    demo: 'px-6 py-3 border-2 border-black rounded-lg hover:bg-black hover:text-white transition-colors inline-flex items-center'
  }[variant];

  return (
    <div className={`${baseClasses} ${className}`}>
      {children}
    </div>
  );
};

export default Card; 