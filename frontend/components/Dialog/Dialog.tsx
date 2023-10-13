import { PropsWithChildren, useState } from 'react';
import { createPortal } from 'react-dom';

export type Disclosure = {
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
  onToggle: () => void;
};

export const useDisclosure = (defaultValue?: boolean): Disclosure => {
  const [isOpen, setIsOpen] = useState<boolean>(!!defaultValue);
  const onOpen = () => setIsOpen(true);
  const onClose = () => setIsOpen(false);
  const onToggle = () => setIsOpen(!isOpen);
  return {
    isOpen,
    onOpen,
    onClose,
    onToggle,
  };
};

export type DialogProps = {
  isOpen?: boolean;
  title?: React.ReactNode;
  closeOnOverlayClick?: boolean;
  onClose?: (() => void) | (() => Promise<void>);
};

const DialogFrame = (props: PropsWithChildren<DialogProps>) => {
  return (
    <>
      <div
        className="fixed inset-0 bg-[#5c5c5c52] transition-opacity"
        style={{ zIndex: 110, backdropFilter: 'blur(10px)' }}
      />
      <div className="fixed inset-0 overflow-y-auto" style={{ zIndex: 111 }}>
        <div
          className="flex min-h-full items-end justify-center p-4 text-center sm:items-center"
          onClick={
            props.closeOnOverlayClick
              ? () => {
                  props.onClose?.();
                }
              : undefined
          }
        >
          <div
            className="flex flex-row justify-center"
            onClick={(e) => {
              e.stopPropagation();
            }}
          >
            <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all min-h-[300px] min-w-[300px] sm:w-full px-4 pt-5 pb-4 sm:p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="text-center sm:text-left">
                    <div className="text-lg pb-4 font-bold text-black">
                      {props.title}
                    </div>
                  </div>
                </div>
                <div>
                  <div className="sm:mt-0">
                    <div
                      role="button"
                      className="inline-block cursor-pointer text-gray-500 hover:text-gray-700"
                      onClick={() => {
                        if (props.onClose !== undefined) props.onClose();
                      }}
                    >
                      <svg
                        stroke="currentColor"
                        fill="none"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="text-gray-900"
                        height="20"
                        width="20"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
              <div className="mt-4 flex flex-col gap-3 text-sm text-gray-600">
                {props.children}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export const DialogPortal = (props: PropsWithChildren<object>) => {
  const elem = document.getElementById('dialog-root');
  if (elem) return createPortal(props.children, elem);
  return <></>;
};

export const Dialog = (props: PropsWithChildren<DialogProps>) => {
  if (!props.isOpen) {
    return <></>;
  }
  return (
    <DialogPortal>
      <DialogFrame {...props} />
    </DialogPortal>
  );
};

export default Dialog;
