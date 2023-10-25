import { IconArrowDown, IconPlayerStop, IconSend } from '@tabler/icons-react';
import {
  KeyboardEvent,
  MutableRefObject,
  useContext,
  useEffect,
  useState,
} from 'react';

import { useTranslation } from 'next-i18next';

import { stopConversation } from '@/utils/app/conversation';

import { Message } from '@/types/chat';
import { LLM, OpenAgent } from '@/types/agent';
import { Plugin } from '@/types/plugin';

import HomeContext from '@/pages/api/home/home.context';

import { MenuItem, Select } from '@mui/material';

interface Props {
  onSend: (message: Message, plugin: Plugin | null) => void;
  onScrollDownClick: () => void;
  textareaRef: MutableRefObject<HTMLTextAreaElement | null>;
  showScrollDownButton: boolean;
  showInputBox: boolean;
}

export const ChatInput = ({
  onSend,
  onScrollDownClick,
  textareaRef,
  showScrollDownButton,
  showInputBox,
}: Props) => {
  const { t } = useTranslation('chat');

  const {
    state: {
      selectedConversation,
      messageIsStreaming,
      chat_id,
      isStopMessageStreaming,
      isStopChatID,
      llmList,
      defaultLLMId,
      isFileUpload,
    },
    dispatch: homeDispatch,
    handleUpdateConversation,
  } = useContext(HomeContext);

  const [content, setContent] = useState<string>();
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const [textareaHeight, setTextareaHeight] = useState(0);

  const [plugin, setPlugin] = useState<Plugin | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    const maxLength = selectedConversation?.agent.maxLength;

    if (maxLength && value.length > maxLength) {
      alert(
        t(
          `Message limit is {{maxLength}} characters. You have entered {{valueLength}} characters.`,
          { maxLength, valueLength: value.length },
        ),
      );
      return;
    }

    setContent(value);
  };

  const handleSend = () => {
    if (messageIsStreaming) {
      return;
    }

    if (!content) {
      alert(t('Please enter a message'));
      return;
    }

    onSend(
      { role: 'user', content, type: '', richContent: null, id: null },
      plugin,
    );
    setContent('');
    setPlugin(null);

    if (window.innerWidth < 640 && textareaRef && textareaRef.current) {
      textareaRef.current.blur();
    }
  };

  const handleStopConversation = async () => {
    homeDispatch({ field: 'isStopMessageStreaming', value: true });
    homeDispatch({ field: 'isStopChatID', value: chat_id });
    await stopConversation(chat_id);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !isTyping && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChangeLLM = async (e: any) => {
    if (!selectedConversation) return;
    const newLLM = llmList.find((llm) => llm.name === e.target.value) as LLM;
    const curModel = selectedConversation.agent as OpenAgent;
    const updateModel = {
      ...curModel,
      llm: newLLM,
    };
    handleUpdateConversation(
      selectedConversation,
      {
        key: 'agent',
        value: updateModel,
      },
      false,
    );
  };

  useEffect(() => {
    if (textareaRef && textareaRef.current) {
      textareaRef.current.style.height = 'inherit';
      textareaRef.current.style.height = `${textareaRef.current?.scrollHeight}px`;
      textareaRef.current.style.overflow = `${
        textareaRef?.current?.scrollHeight > 350 ? 'auto' : 'hidden'
      }`;
    }
  }, [content]);

  useEffect(() => {
    if (textareaRef.current) {
      setTextareaHeight(textareaRef.current.clientHeight);
    }
  }, [content]);

  return (
    <div className="absolute bottom-0 left-0 w-full border-transparent pt-2 z-[99] bg-transparent">
      <div className="stretch w-full px-20 mt-4 flex flex-row gap-3">
        {messageIsStreaming &&
          !isFileUpload &&
          !(isStopMessageStreaming && isStopChatID === chat_id) && (
            <button
              className="absolute h-8 top-[-13px] left-0 right-0 mx-auto border border-[#c4c4c4] bg-white flex w-fit items-center gap-3 rounded-xl py-2 px-4 text-black hover:opacity-50"
              onClick={handleStopConversation}
            >
              <IconPlayerStop size={16} /> {t('Stop generating')}
            </button>
          )}

        {!messageIsStreaming &&
          isStopMessageStreaming &&
          isStopChatID === chat_id && (
            <div className="absolute h-8 top-[-20px] left-0 right-0 mx-auto flex w-fit items-center gap-3 py-2 px-4 text-red-500 text-xl">
              Response successfully stopped! Please edit your message or retry.
            </div>
          )}

        <div className="relative flex flex-grow flex-col border rounded-xl border-black/10 bg-white shadow-[0_0_10px_rgba(0,0,0,0.10)]">
          {!messageIsStreaming && showInputBox && (
            <>
              <div
                className={`absolute left-0 min-w-[170px] rounded-xl pr-2 text-neutral-900`}
                style={{ bottom: textareaHeight + 6 + 'px' }}
              >
                <Select
                  className="w-full p-2 h-8 font-[Montserrat] bg-white rounded-xl"
                  value={selectedConversation?.agent?.llm?.id || defaultLLMId}
                  onChange={handleChangeLLM}
                  MenuProps={{
                    anchorOrigin: {
                      vertical: 'top',
                      horizontal: 'center',
                    },
                    transformOrigin: {
                      vertical: 'bottom',
                      horizontal: 'center',
                    },
                    PaperProps: {
                      className: 'rounded-xl -mt-1',
                      sx: {
                        '& .MuiMenuItem-root': {
                          fontFamily: 'Montserrat',
                        },
                      },
                    },
                  }}
                >
                  {llmList.map((llm) => (
                    <MenuItem
                      key={llm.id}
                      value={llm.name}
                      className="rounded-xl"
                    >
                      {llm.name}
                    </MenuItem>
                  ))}
                </Select>
              </div>
            </>
          )}

          {showInputBox && (
            <textarea
              ref={textareaRef}
              className="m-0 w-full resize-none border-0 bg-transparent p-0 py-2 pr-2 pl-10 text-black md:py-3 md:pl-3 placeholder:text-[#7E7E7E] focus:outline-none focus:border-[#212121] focus:ring-[#212121] focus:ring-1 rounded-xl"
              style={{
                resize: 'none',
                bottom: `${textareaRef?.current?.scrollHeight}px`,
                maxHeight: '350px',
                overflow: `${
                  textareaRef.current && textareaRef.current.scrollHeight > 350
                    ? 'auto'
                    : 'hidden'
                }`,
              }}
              placeholder={'Send a message'}
              value={content}
              rows={1}
              onCompositionStart={() => setIsTyping(true)}
              onCompositionEnd={() => setIsTyping(false)}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
            />
          )}
          {showInputBox && (
            <button
              className="absolute right-[5px] top-[5px] rounded-xl text-neutral-800"
              onClick={handleSend}
            >
              {messageIsStreaming ? (
                <div className="h-6 w-6 mt-1 mr-1 animate-spin rounded-full border-t-2 border-neutral-800 opacity-60"></div>
              ) : (
                <IconSend size={26} className="mt-1 mr-1" />
              )}
            </button>
          )}

          {showInputBox && showScrollDownButton && (
            <div className="absolute bottom-2 -right-10">
              <button
                className="flex h-7 w-7 items-center justify-center rounded-full bg-neutral-300 text-gray-800 shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={onScrollDownClick}
              >
                <IconArrowDown size={18} />
              </button>
            </div>
          )}
        </div>
      </div>

      <div className="px-3 pt-2 pb-3 text-center text-[12px] text-black/50 md:px-4 md:pt-3 md:pb-6 bg-[#F3F3F3]">
        Powered by&nbsp;
        <a
          href="https://xlang.ai"
          target="_blank"
          rel="noreferrer"
          className="underline"
        >
          XLang Team
        </a>
        .
      </div>
    </div>
  );
};
