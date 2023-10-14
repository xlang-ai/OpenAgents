import { IconCircleCheck, IconSend } from '@tabler/icons-react';
import { MutableRefObject, useContext, useEffect, useState } from 'react';

import { useTranslation } from 'next-i18next';

import { Plugin } from '@/types/plugin';

import HomeContext from '@/pages/api/home/home.context';

interface Props {
  onConfirm: (apiKey: string) => void;
  textareaRef: MutableRefObject<HTMLTextAreaElement | null>;
  currentPlugin: Plugin;
}

export const ApiKeyInput = ({
  onConfirm,
  textareaRef,
  currentPlugin,
}: Props) => {
  const { t } = useTranslation('chat');

  const {
    state: { apiKeyUploading },
  } = useContext(HomeContext);

  const [content, setContent] = useState<string>(currentPlugin?.api_key ?? '');
  const [rerender, setRerender] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setContent(value);
  };
  const handleSend = () => {
    if (apiKeyUploading) {
      return;
    }
    if (!content) {
      alert(t('Please enter a api key'));
      return;
    }
    onConfirm(content);
  };
  useEffect(() => {
    if (textareaRef && textareaRef.current) {
      textareaRef.current.style.height = 'inherit';
      textareaRef.current.style.height = `${textareaRef.current?.scrollHeight}px`;
      textareaRef.current.style.overflow = `${
        textareaRef?.current?.scrollHeight > 400 ? 'auto' : 'hidden'
      }`;
    }
  }, [content]);
  useEffect(() => {
    setContent(currentPlugin?.api_key ?? '');
  }, [currentPlugin]);
  useEffect(() => {
    setRerender(content == currentPlugin.api_key);
  }, [apiKeyUploading, content, currentPlugin]);
  return (
    <div className="relative flex text-sm w-full h-10 flex-grow flex-col rounded-md border border-black/10 bg-white shadow-[0_0_10px_rgba(0,0,0,0.10)]">
      <textarea
        ref={textareaRef}
        className="m-0 w-full items-center h-10 leading-10 resize-none border-1 bg-transparent pl-2 pr-8 text-black"
        placeholder={t('Type your API key') || ''}
        value={content}
        rows={1}
        onChange={handleChange}
      />
      <button
        className="absolute right-2 top-2 rounded-sm p-1 text-neutral-800 opacity-60 hover:bg-neutral-200 hover:text-neutral-900"
        onClick={rerender ? () => {} : handleSend}
      >
        {apiKeyUploading ? (
          <div className="h-4 w-4 animate-spin rounded-full border-t-2 border-neutral-800 opacity-60"></div>
        ) : rerender ? (
          <IconCircleCheck
            size={18}
            className="text-[#32CD32]"
          ></IconCircleCheck>
        ) : (
          <IconSend size={18}></IconSend>
        )}
      </button>
    </div>
  );
};
