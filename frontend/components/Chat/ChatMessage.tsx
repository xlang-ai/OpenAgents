import {
  IconCircleCheck,
  IconCircleX,
  IconCopy,
  IconEdit,
  IconRepeat,
} from '@tabler/icons-react';
import React, {
  FC,
  ReactNode,
  memo,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react';
import toast from 'react-hot-toast';
import ReactMarkdown from 'react-markdown';

import { useTranslation } from 'next-i18next';

import { saveConversation } from '@/utils/app/conversation';

import { Message } from '@/types/chat';

import HomeContext from '@/pages/api/home/home.context';

import ChatRichContentItem from '@/components/Chat/ChatRichContentItem';

import { ToolCollapse } from './ToolCollapse';

import RobotIcon from '@/icons/RobotIcon';
import webotIconURL from '@/public/webot_icon_base64';
import ExtensionOutlinedIcon from '@mui/icons-material/ExtensionOutlined';
import PersonIcon from '@mui/icons-material/Person';
import List from '@mui/material/List';
import Paper from '@mui/material/Paper';
import clipboardCopy from 'clipboard-copy';

export interface Props {
  message: Message;
  messageIndex: number;
  onEdit?: (editedMessage: Message) => void;
  onRegenerate?: () => void;
  scrollToBottom?: () => void;
}
export interface MessageCardInfo {
  title: string;
  webLink: string;
  imageLink: string;
}

export const checkJsonString = (str: string) => {
  /* return false if input is not a json string ; return the json object if input is a json string */
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
};

export const ChatMessage: FC<Props> = memo(
  ({ message, messageIndex, onEdit, onRegenerate, scrollToBottom }) => {
    const {
      state: {
        selectedConversation,
        messageIsStreaming,
        isStreamingMessageId,
        selectedPlugins,
        pluginList,
        showChatbar,
      },
      dispatch: homeDispatch,
    } = useContext(HomeContext);

    const [isEditing, setIsEditing] = useState<boolean>(false);
    const [isTyping, setIsTyping] = useState<boolean>(false);
    const [messageContent, setMessageContent] = useState(message.content);
    const [userMsgWidth, setUserMsgWidth] = useState<number>(0);

    const textareaRef = useRef<HTMLTextAreaElement>(null);
    const userMsgRef = useRef<HTMLDivElement>(null);
    const aiMsgRef = useRef<HTMLDivElement>(null);

    const toggleEditing = () => {
      setIsEditing(!isEditing);
    };

    const handleInputChange = (
      event: React.ChangeEvent<HTMLTextAreaElement>,
    ) => {
      setMessageContent(event.target.value);
      if (textareaRef.current) {
        textareaRef.current.style.height = 'inherit';
        textareaRef.current.style.height = `${textareaRef.current.clientHeight}px`;
      }
    };

    const handleEditMessage = () => {
      if (message.content != messageContent) {
        if (selectedConversation && onEdit) {
          onEdit({ ...message, content: messageContent });
        }
      }
      setIsEditing(false);
      setShowButtons(false);
    };

    const handleCopyMessage = () => {
      if (
        message?.richContent?.intermediateSteps &&
        message?.richContent?.intermediateSteps?.length > 0
      ) {
        clipboardCopy(
          message.richContent.intermediateSteps[
            message.richContent.intermediateSteps.length - 1
          ].content,
        );
      } else {
        clipboardCopy(message.content);
      }
      toast.success('Copied!');
    };

    const handlePressEnter = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !isTyping && !e.shiftKey) {
        e.preventDefault();
        handleEditMessage();
      }
    };

    useEffect(() => {
      setMessageContent(message.content);
    }, [message.content]);

    useEffect(() => {
      if (textareaRef.current) {
        textareaRef.current.style.height = 'inherit';
        textareaRef.current.style.height = `${textareaRef.current.clientHeight}px`;
      }
    }, [isEditing]);

    const renderRichIntermediateSteps = () => {
      if (!selectedConversation) return null;
      if (!message.richContent?.intermediateSteps) return null;
      let result = [] as ReactNode[];

      let curIndex = 0;
      const toolCollapseTypes = ['plain', 'execution_result'];
      while (curIndex < message.richContent.intermediateSteps.length) {
        let item = message.richContent.intermediateSteps[curIndex];
        if (item.type == 'tool') {
          let curToolName = item.content.replace(/\*/g, '');
          let curToolIcon;
          let curToolEndIndex =
            message.richContent?.intermediateSteps.findIndex(
              (item, index) =>
                index > curIndex && !toolCollapseTypes.includes(item.type),
            );
          let curToolSteps =
            curToolEndIndex == -1
              ? message.richContent.intermediateSteps.slice(curIndex)
              : message.richContent.intermediateSteps.slice(
                  curIndex,
                  curToolEndIndex,
                );
          let allEnabledPlugins = [
            ...selectedConversation.selectedPlugins,
            ...selectedConversation.selectedCodeInterpreterPlugins,
          ];
          let curTool;

          // get the tool currently being used
          if (
            selectedPlugins.length == 1 &&
            selectedPlugins[0].name == 'auto'
          ) {
            curTool = pluginList.find(
              (plugin) =>
                plugin.name.replace(/\*/g, '').toLowerCase() ==
                curToolName.toLowerCase(),
            );
          } else {
            curTool = allEnabledPlugins.find(
              (plugin) =>
                plugin.name.replace(/\*/g, '').toLowerCase() ==
                curToolName.toLowerCase(),
            );
          }

          // the tool is Webot
          if (curToolName == 'WeBot') {
            curToolIcon = (
              <img
                className={`text-[#343541] mt-1 ml-1 ${'!h-5 !w-5'}`}
                src={webotIconURL}
              />
            );
          }
          // get the icon of the tool currently being used
          else if (curTool == undefined) {
            curToolIcon = (
              <ExtensionOutlinedIcon
                className={`text-[#343541] ${'!h-5 !w-5'}`}
              />
            );
          }
          // the tool is selected by Auto
          else if (
            selectedPlugins.length == 1 &&
            selectedPlugins[0].name == 'auto'
          ) {
            curToolIcon = (
              <img
                className={`text-[#343541] mt-1 ml-1 ${'!h-5 !w-5'}`}
                src={curTool.icon}
                alt={curTool.name}
              />
            );
          } else {
            curToolIcon = (
              <img
                className={`text-[#343541] mt-1 ml-1 ${'!h-5 !w-5'}`}
                src={curTool.icon}
                alt={curTool.name}
              />
            );
          }
          result.push(
            <div
              className={`${
                showChatbar
                  ? 'w-[calc(100vw-260px-21.5rem)]'
                  : 'w-[calc(100vw-26.8rem)]'
              } ml-[-3px]`}
            >
              <ToolCollapse
                content={
                  <List component="div" disablePadding className="w-full">
                    {curToolSteps.map((listItem, listIndex) => {
                      if (listItem.type != 'tool') {
                        return (
                          <li
                            key={listItem.id}
                            className="group/rich-item max-w-full mb-2"
                          >
                            <div className="max-w-full">
                              <ChatRichContentItem
                                item={listItem}
                                itemIndex={listIndex + curIndex}
                                messageIndex={messageIndex}
                                component={'intermediateSteps'}
                              ></ChatRichContentItem>
                            </div>
                          </li>
                        );
                      }
                    })}
                  </List>
                }
                toolName={
                  curTool
                    ? 'prettyNameForHuman' in curTool
                      ? curTool.prettyNameForHuman
                      : curTool.nameForHuman
                    : curToolName
                }
                icon={curToolIcon}
                pluginUsing={
                  messageIndex == isStreamingMessageId &&
                  curToolEndIndex == -1 &&
                  message.richContent.finalAnswer.length == 0 &&
                  messageIsStreaming
                }
              />
            </div>,
          );
          curIndex += curToolSteps.length;
        } else {
          result.push(
            <ChatRichContentItem
              item={item}
              itemIndex={curIndex}
              messageIndex={messageIndex}
              component={'intermediateSteps'}
            />,
          );
          curIndex += 1;
        }
      }
      return result;
    };

    const [showButtons, setShowButtons] = useState(false);
    const handleMouseEnter = () => {
      setShowButtons(true);
    };

    const handleMouseLeave = () => {
      setShowButtons(false);
    };

    useEffect(() => {
      !isEditing && setUserMsgWidth(userMsgRef.current?.clientWidth || 0);
      messageIsStreaming && scrollToBottom && scrollToBottom();
    }, [userMsgRef.current?.clientWidth, userMsgRef.current?.clientHeight]);

    useEffect(() => {
      messageIsStreaming && scrollToBottom && scrollToBottom();
    }, [aiMsgRef.current?.clientWidth, aiMsgRef.current?.clientHeight]);

    return (
      <div
        className={`w-full bg-[#F3F3F3] text-[#011020] relative flex items-end
          ${message.role === 'user' ? 'justify-end' : 'justify-start'}
        `}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {message.role === 'assistant' && (
          <RobotIcon
            className={`rounded-full ml-28 mb-[13px]`}
            width={30}
            height={30}
          />
        )}

        <Paper
          elevation={3}
          className={`relative w-fit ${
            showChatbar
              ? 'max-w-[calc(100vw-260px-20.4rem)]'
              : 'max-w-[calc(100vw-25.7rem)]'
          } my-4 flex items-center p-3 text-base rounded-2xl
          ${
            message.role === 'user'
              ? 'bg-[#E2E2E2] mr-4 ml-40'
              : 'bg-white ml-4 mr-40'
          }`}
        >
          {message.role === 'user' && (
            <div className="w-full">
              {isEditing && message.type !== 'rich_message' ? (
                <div className={`flex flex-col w-[${userMsgWidth}px]`}>
                  {/* plain msgs editing */}
                  <textarea
                    ref={textareaRef}
                    className={`min-w-[200px] resize-none whitespace-pre-wrap border-none bg-[#E2E2E2]`}
                    style={{ width: `${userMsgWidth}px` }}
                    value={messageContent}
                    onChange={handleInputChange}
                    onKeyDown={handlePressEnter}
                    onCompositionStart={() => setIsTyping(true)}
                    onCompositionEnd={() => setIsTyping(false)}
                  />

                  <div className="flex space-x-4 justify-end mt-[2px]">
                    <button
                      className="flex"
                      onClick={handleEditMessage}
                      disabled={messageContent.trim().length <= 0}
                    >
                      <IconCircleCheck size={20} color="#7B7B7B" />
                      <span className="text-xs text-[#7B7B7B] font-[600] mt-[3px]">
                        Submit
                      </span>
                    </button>
                    <button
                      className="flex"
                      onClick={() => {
                        setMessageContent(message.content);
                        setIsEditing(false);
                        setShowButtons(false);
                      }}
                    >
                      <IconCircleX size={20} color="#7B7B7B" />
                      <span className="text-xs text-[#7B7B7B] font-[600] mt-[3px]">
                        Cancel
                      </span>
                    </button>
                  </div>
                </div>
              ) : message.type === 'rich_message' ? (
                // render rich msgs like tables, images
                <>
                  {message.richContent &&
                    message.richContent.finalAnswer?.length > 0 &&
                    message.richContent.finalAnswer.map((item, index) => {
                      return (
                        <React.Fragment key={item.id}>
                          <div className="mt-[5px] w-full">
                            <ChatRichContentItem
                              item={item}
                              itemIndex={index}
                              messageIndex={messageIndex}
                              component={'finalAnswer'}
                            ></ChatRichContentItem>
                          </div>
                        </React.Fragment>
                      );
                    })}
                </>
              ) : (
                // plain msgs
                <div ref={userMsgRef} className="prose w-full max-w-full">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>
              )}

              {/* edit and copy btns */}
              {!isEditing && message.type !== 'rich_message' && showButtons && (
                <div className="flex z-[999] absolute bottom-[-23px] right-1">
                  {!messageIsStreaming && (
                    <button className="flex" onClick={toggleEditing}>
                      <IconEdit color="#7B7B7B" size={20} />
                      <span className="text-xs text-[#7B7B7B] font-[600] ml-1 mt-[3px]">
                        Edit
                      </span>
                    </button>
                  )}
                  <button className="flex ml-3" onClick={handleCopyMessage}>
                    <IconCopy color="#7B7B7B" size={20} />
                    <span className="text-xs text-[#7B7B7B] font-[600] ml-1 mt-[3px]">
                      Copy
                    </span>
                  </button>
                </div>
              )}
            </div>
          )}

          {message.role === 'assistant' && (
            <div ref={aiMsgRef} className="max-w-full">
              {/* render rich msgs containing tool use steps */}
              {message.type === 'rich_message' &&
                message.richContent &&
                message.richContent.intermediateSteps?.length > 0 && (
                  <>{renderRichIntermediateSteps()}</>
                )}

              {/* render final answer (plain text) */}
              {message.type === 'rich_message' &&
                message.richContent &&
                message.richContent.finalAnswer?.length > 0 &&
                message.richContent.finalAnswer
                  .filter((item) => {
                    return item.type != 'card_info';
                  })
                  .map((item, index) => {
                    return (
                      <React.Fragment key={item.id}>
                        <div className="mt-[5px] w-full">
                          <ChatRichContentItem
                            item={item}
                            itemIndex={index}
                            messageIndex={messageIndex}
                            component={'finalAnswer'}
                          ></ChatRichContentItem>
                        </div>
                      </React.Fragment>
                    );
                  })}

              {/* render card info (output by specific plugins) */}
              <div className="flex overflow-x-auto overflow-y-hidden">
                {selectedConversation?.agent.id == 'plugins-agent' &&
                  message.type === 'rich_message' &&
                  message.richContent &&
                  message.richContent.finalAnswer?.length > 0 &&
                  message.richContent.finalAnswer
                    .filter((item) => {
                      return item.type == 'card_info';
                    })
                    .map((item) => {
                      const js = JSON.parse(item.content);
                      const title = js.title;
                      const imageLink = js.image_link;
                      const webLink = js.web_link;
                      if (imageLink != '') {
                        return (
                          <div
                            className="flex flex-col shrink-0 rounded-xl border border-[#D8D8D8] p-3 space-y-2 ml-4 mb-2 w-[300px] h-48 cursor-pointer"
                            onClick={() => {
                              window.open(webLink);
                            }}
                          >
                            <img
                              alt="item"
                              src={imageLink}
                              className="w-[100px]"
                            />
                            <div className="text-sm font-[600]">{title}</div>
                          </div>
                        );
                      }
                    })}
                {message.type === 'alert_message' && (
                  <span className="text-red-500">{message.content}</span>
                )}
              </div>

              {/* copy and retry btns*/}
              {showButtons && (
                <div className="flex z-[999] absolute bottom-[-23px] left-1">
                  <button className="flex" onClick={handleCopyMessage}>
                    <IconCopy color="#7B7B7B" size={20} />
                    <span className="text-xs text-[#7B7B7B] font-[600] ml-1 mt-[3px]">
                      Copy
                    </span>
                  </button>
                  {!messageIsStreaming &&
                    selectedConversation &&
                    selectedConversation.messages.length > 0 && (
                      <button className="flex ml-3" onClick={onRegenerate}>
                        <IconRepeat color="#7B7B7B" size={20} />
                        <span className="text-xs text-[#7B7B7B] font-[600] ml-1 mt-[3px]">
                          Retry
                        </span>
                      </button>
                    )}
                </div>
              )}
            </div>
          )}
        </Paper>

        {message.role === 'user' && (
          <PersonIcon className="bg-[#4B2E83] w-8 h-8 text-white p-1 rounded-full mr-28 mb-[13px]" />
        )}
      </div>
    );
  },
);
ChatMessage.displayName = 'ChatMessage';
