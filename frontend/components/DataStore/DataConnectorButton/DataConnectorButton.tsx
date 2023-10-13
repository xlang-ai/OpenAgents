import React from 'react';

interface DataConnectorButtonProps {
  name: string;
  icon: JSX.Element;
  onClick: () => void;
}

const DataConnectorButton = ({
  name,
  icon,
  onClick,
}: DataConnectorButtonProps) => {
  return (
    <button
      className="flex w-full cursor-pointer items-center gap-2 rounded-lg p-2 text-sm transition-colors duration-200 hover:bg-[#343541]/90 group"
      onClick={onClick}
    >
      <div className="h-5 w-5">{icon}</div>
      <span>{name}</span>
      <span className="ml-auto text-blue-500 hidden group-hover:block">
        Connect
      </span>
    </button>
  );
};

export default DataConnectorButton;
