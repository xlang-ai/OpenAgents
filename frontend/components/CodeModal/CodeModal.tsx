import { IconCheck, IconCircleFilled, IconX } from '@tabler/icons-react';
import CodeMirror from '@uiw/react-codemirror';
import React, { useContext, useState } from 'react';
import { createPortal } from 'react-dom';
import { Rnd } from 'react-rnd';

import { saveConversation } from '@/utils/app/conversation';

import { Conversation, RichContentItemType } from '@/types/chat';

import HomeContext from '@/pages/api/home/home.context';

import { ChatRichContentItemBody } from '../Chat/ChatRichContentItem';

import { python } from '@codemirror/lang-python';
import { okaidia } from '@uiw/codemirror-theme-okaidia';
import { EditorView } from 'codemirror';

const CodeModal = ({
  setOpenModal,
  code,
  setCode,
  component,
  messageIndex,
  itemIndex,
  language,
}: {
  setOpenModal: React.Dispatch<React.SetStateAction<boolean>>;
  code: string;
  setCode: React.Dispatch<React.SetStateAction<string>>;
  component: string;
  messageIndex: number;
  itemIndex: number;
  language: string;
}) => {
  const {
    state: { selectedConversation, messageIsStreaming },
    dispatch,
  } = useContext(HomeContext);
  const [executionResult, setExecutionResult] = useState<{
    content: string;
    type: string;
  }>();
  const [_code, _setCode] = useState<string>(code);

  const confirmEdit = () => {
    setOpenModal(false);
    const updatedConversation: Conversation = JSON.parse(
      JSON.stringify(selectedConversation),
    );
    setCode(_code);
    if (component === 'intermediateSteps') {
      updatedConversation.messages[messageIndex].richContent!.intermediateSteps[
        itemIndex
      ].content = `\`\`\`${language}\n${_code}\n\`\`\``;
    } else {
      updatedConversation.messages[messageIndex].richContent!.finalAnswer[
        itemIndex
      ].content = `\`\`\`${language}\n${_code}\n\`\`\``;
    }
    updatedConversation.messages[
      messageIndex
    ].content = `\`\`\`${language}\n${_code}\n\`\`\``;
    dispatch({ field: 'selectedConversation', value: updatedConversation });
    saveConversation(updatedConversation);
  };

  const cancelEdit = () => {
    setOpenModal(false);
  };

  return createPortal(
    <Rnd
      dragHandleClassName="handle"
      className="z-[9999] shadow-lg"
      default={{
        x: window.innerWidth / 2,
        y: window.innerHeight / 4,
        width: window.innerWidth / 3,
        height: window.innerHeight / 3,
      }}
    >
      <div className="bg-[#343541] w-full h-full text-white rounded-lg overflow-hidden pb-2">
        <div className="handle cursor-grab flex justify-between items-center bg-[#202123] p-1">
          <div className="flex gap-1">
            <IconCircleFilled size={12} className="text-red-500/80" />
            <IconCircleFilled size={12} className="text-yellow-500/80" />
            <IconCircleFilled size={12} className="text-green-500/80" />
          </div>
          <div className="flex gap-1 mr-1">
            <IconX
              size={14}
              className="opacity-80 hover:opacity-100 cursor-pointer"
              onClick={cancelEdit}
            />
            <IconCheck
              size={14}
              className="opacity-80 hover:opacity-100 cursor-pointer"
              onClick={confirmEdit}
            />
          </div>
        </div>
        <div className="py-1 px-2 overflow-y-auto h-full pb-7">
          <CodeMirror
            onKeyDown={(event) => {
              if (event.keyCode == 13 && event.shiftKey) {
                event.preventDefault();
              }
            }}
            value={_code}
            extensions={[python(), EditorView.lineWrapping]}
            theme={okaidia}
            onChange={(_code) => _setCode(_code)}
          />

          {executionResult && (
            <div className="text-sm bg-[#40414f] text-sm rounded overflow-hidden mt-4 shadow-sm">
              <div className="font-bold bg-[#202123] px-2 py-1 flex items-center justify-between">
                <span>Execution results</span>
                <IconX
                  size={14}
                  className="opacity-80 hover:opacity-100 cursor-pointer"
                  onClick={() => setExecutionResult(undefined)}
                />
              </div>
              <div className="p-2 overflow-auto">
                <ChatRichContentItemBody
                  item={{
                    content: executionResult.content,
                    type: executionResult.type as RichContentItemType,
                    id: -1,
                    message_id: null,
                  }}
                  messageIsStreaming={messageIsStreaming}
                  component={component}
                  messageIndex={messageIndex}
                  itemIndex={itemIndex}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </Rnd>,
    document.body,
  );
};

export default CodeModal;
