import React, { useContext } from 'react';

import { AgentSelect } from './AgentSelect';

interface SettingsModalProps {
  setIsSettingsModalOpen: (isSettingsModalOpen: boolean) => void;
}

export const SettingsModal = (props: SettingsModalProps) => {
  const { setIsSettingsModalOpen } = props;

  return (
    <>
      {/* Translucent Background */}
      <div
        className="!mt-0 bg-black bg-opacity-50 z-10 absolute top-0 right-0 bottom-0 left-0"
        id="settings-modal"
      >
        <div className="w-full h-full flex justify-center items-start px-2 md:px-12 p-12">
          {/* Modal */}
          <div
            role="alert"
            className="container mx-auto w-11/12 md:w-2/3 inline-block"
          >
            <div className="relative py-8 px-5 md:px-10 bg-[#202123] shadow-md rounded max-w-full">
              <div className="text-neutral-400 text-lg">Settings</div>
              <div className="pt-12">
                <AgentSelect />
              </div>
              <div className="mt-12"></div>

              {/* Close Icon */}
              <button
                className="cursor-pointer absolute top-0 right-0 mt-4 mr-5 text-gray-400 hover:text-gray-600 transition duration-150 ease-in-out rounded focus:ring-2 focus:outline-none focus:ring-gray-600"
                onClick={() => setIsSettingsModalOpen(false)}
                aria-label="close modal"
                role="button"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="icon icon-tabler icon-tabler-x"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  strokeWidth="2.5"
                  stroke="currentColor"
                  fill="none"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path stroke="none" d="M0 0h24v24H0z" />
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
