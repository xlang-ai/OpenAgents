import {
  MutableRefObject,
  memo,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react';
import toast from 'react-hot-toast';

import { useTranslation } from 'next-i18next';

import {
  API_CHAT_XLANG_WEBOT_RESET_STATUS,
  API_CHAT_XLANG_WEBOT_STATUS,
} from '@/utils/app/const';
import { throttle } from '@/utils/data/throttle';

import { Message } from '@/types/chat';

import HomeContext from '@/pages/api/home/home.context';

import { ChatInput } from './ChatInput';
import { ChatLoader } from './ChatLoader';
import { ChatMessage } from './ChatMessage';
import { CodeInterpreterPluginSelect } from './CodeInterpreterPluginSelect';
import { ErrorMessageDiv } from './ErrorMessageDiv';
import { AgentSelect } from './AgentSelect';
import { PluginSelect } from './PluginSelect';
import { QuestionSuggestion } from './QuestionSuggestion';
import { SettingsModal } from './SettingsModal';
import { TemperatureSlider } from './Temperature';

import { HelpOutlineOutlined } from '@mui/icons-material';
import ExtensionOutlinedIcon from '@mui/icons-material/ExtensionOutlined';
import Paper from '@mui/material/Paper';
import Tooltip from '@mui/material/Tooltip';

interface Props {
  stopConversationRef: MutableRefObject<boolean>;
}

export const Chat = memo(({ stopConversationRef }: Props) => {
  const { t } = useTranslation('chat');

  const {
    state: {
      chat_id,
      selectedConversation,
      apiKey,
      pluginKeys,
      messageIsStreaming,
      modelError,
      loading,
      followUpQuestions,
      followUpLoading,
      selectedPlugins,
      conversationNameList,
      selectedCodeInterpreterPlugins,
      isStopMessageStreaming,
      isStopChatID,
      isStreamingError,
      isStreamingErrorChatID,
      recommendChatID,
    },
    handleUpdateConversation,
    handleSend: _handleSend,
    dispatch: homeDispatch,
  } = useContext(HomeContext);

  const [currentMessage, setCurrentMessage] = useState<Message>();
  const [autoScrollEnabled, setAutoScrollEnabled] = useState<boolean>(true);
  const [showSettings, setShowSettings] = useState<boolean>(false);
  const [showScrollDownButton, setShowScrollDownButton] =
    useState<boolean>(false);
  const [showInputBox, setShowInputBox] = useState<boolean>(true);
  const [pollingExists, setPollingExists] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const tooltips = {
    Agent:
      'OpenAgents empowers you to transform your human Lang(uage) into X(utable) actions, and help you with real-world tasks, e.g., data-related.',
    Plugins:
      'Plugins are tools designed to help OpenAgents access up-to-date information, run computations, or use third-party services.',
    Temperature:
      'Temperature controls randomness. Lowering it results in less random completions. As it approaches zero, the model will become deterministic and repetitive.',
  };

  const handleSend = useCallback(_handleSend, [
    apiKey,
    pluginKeys,
    conversationNameList,
    selectedConversation,
    stopConversationRef,
    selectedPlugins,
    selectedCodeInterpreterPlugins,
    isStopChatID,
    isStopMessageStreaming,
  ]);
  const resetWebot = async () => {
    let res;
    try {
      res = await fetch(API_CHAT_XLANG_WEBOT_RESET_STATUS, {
        method: 'POST',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chat_id: chat_id,
        }),
      });
    } catch (error) {
      homeDispatch({ field: 'loading', value: false });
      homeDispatch({ field: 'messageIsStreaming', value: false });
      toast.error((error as Error).message);
      return;
    }
    if (!res.ok) {
      homeDispatch({ field: 'loading', value: false });
      homeDispatch({ field: 'messageIsStreaming', value: false });
      toast.error(res.statusText);
      return;
    }
    const data = await res.json();
    if (data['chat_id'] != chat_id) {
      toast.error('Error during resetting webot', {
        id: chat_id,
      });
      throw new Error('Error during resetting webot');
    }
  };

  const pollingWebotStatus = async () => {
    if (
      messageIsStreaming == true &&
      selectedConversation?.agent.id == 'web_agent' &&
      !pollingExists
    ) {
      const startTime = Date.now();
      setPollingExists(true);
      let count = 0;
      while (true) {
        if (
          (isStopMessageStreaming && isStopChatID == chat_id) ||
          !messageIsStreaming
        ) {
          break;
        }
        let res;
        try {
          res = await fetch(API_CHAT_XLANG_WEBOT_STATUS, {
            method: 'POST',
            headers: {
              'Access-Control-Allow-Origin': '*',
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              chat_id: chat_id,
            }),
          });
        } catch (error) {
          homeDispatch({ field: 'loading', value: false });
          homeDispatch({ field: 'messageIsStreaming', value: false });
          toast.error((error as Error).message);
          return;
        }
        const data = await res.json();
        if (data['webot_status'] == 'running') {
          try {
            await resetWebot();
            let countdown = 3;
            const countdownToast = async () => {
              if (countdown > 0) {
                toast.loading(`Going to web search page in ${countdown}s...`, {
                  id: chat_id,
                });
                countdown--;
                setTimeout(() => {
                  countdownToast();
                }, 1000);
              } else {
                toast.remove();
                window.open(data['url']);
              }
            };
            countdownToast();
            break;
          } catch (error) {
            homeDispatch({ field: 'loading', value: false });
            homeDispatch({ field: 'messageIsStreaming', value: false });
            toast.error((error as Error).message);
            return;
          }
        }
        await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait for 2 seconds before the next iteration
        count++;
        // Check if 2 minutes have passed
        if (Date.now() - startTime > 2 * 60 * 1000) {
          break; // Stop the loop
        }
      }
      setPollingExists(false);
    }
  };

  const scrollToBottom = useCallback(() => {
    if (autoScrollEnabled) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [autoScrollEnabled]);

  const handleScroll = () => {
    if (chatContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } =
        chatContainerRef.current;
      const bottomTolerance = 30;

      if (scrollTop + clientHeight < scrollHeight - bottomTolerance) {
        setAutoScrollEnabled(false);
        setShowScrollDownButton(true);
      } else {
        setAutoScrollEnabled(true);
        setShowScrollDownButton(false);
      }
    }
  };

  const handleScrollDown = () => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  };

  const handleSettings = () => {
    setShowSettings(!showSettings);
  };

  const onClearAll = () => {
    if (
      confirm(t<string>('Are you sure you want to clear all messages?')) &&
      selectedConversation
    ) {
      handleUpdateConversation(
        selectedConversation,
        {
          key: 'messages',
          value: [],
        },
        false,
      );
    }
  };

  const scrollDown = () => {
    if (autoScrollEnabled) {
      messagesEndRef.current?.scrollIntoView(true);
    }
  };
  const throttledScrollDown = throttle(scrollDown, 250);

  useEffect(() => {
    selectedConversation &&
      setCurrentMessage(
        selectedConversation.messages[selectedConversation.messages.length - 2],
      );
  }, [selectedConversation, throttledScrollDown]);

  const handleRegenerate = () => {
    if (currentMessage) {
      handleSend(currentMessage, 2, true, null, null, true);
      if (isStopMessageStreaming && isStopChatID == chat_id) {
        homeDispatch({ field: 'isStopMessageStreaming', value: false });
        homeDispatch({ field: 'isStopChatID', value: '' });
      }
    }
  };

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setAutoScrollEnabled(entry.isIntersecting);
      },
      {
        root: null,
        threshold: 0.5,
      },
    );
    const messagesEndElement = messagesEndRef.current;
    if (messagesEndElement) {
      observer.observe(messagesEndElement);
    }
    return () => {
      if (messagesEndElement) {
        observer.unobserve(messagesEndElement);
      }
    };
  }, [messagesEndRef]);

  useEffect(() => {
    if (selectedConversation?.id) pollingWebotStatus();
  }, [messageIsStreaming, selectedConversation?.id]);

  useEffect(() => {
    setShowInputBox(
      !(isStreamingError && isStreamingErrorChatID == chat_id) &&
        !(isStopMessageStreaming && isStopChatID == chat_id),
    );
  }, [
    isStreamingError,
    isStreamingErrorChatID,
    chat_id,
    isStopMessageStreaming,
    isStopChatID,
  ]);

  return (
    <div className="relative flex-1 overflow-hidden bg-[#F3F3F3]">
      {modelError ? (
        <ErrorMessageDiv error={modelError} />
      ) : (
        <>
          <div
            className="max-h-full w-full overflow-y-auto overflow-x-hidden"
            ref={chatContainerRef}
            onScroll={handleScroll}
          >
            {selectedConversation?.messages.length === 0 ? (
              <>
                <div className="flex flex-col space-y-5 w-full h-full">
                  <div className="pl-20 pt-16 space-y-5">
                    <div className="text-left text-3xl font-[500] text-gray-800">
                      Hi!
                    </div>
                    <div className="text-left text-lg font-[500] text-gray-800">
                      Please choose your Agent & Plugins to continue
                    </div>
                  </div>

                  <div className="flex items-center justify-center pt-8 pb-2 text-lg">
                    <Paper className="w-[50rem] space-y-6 rounded-xl p-8 shadow-md">
                      <div className="flex relative">
                        <span className="font-[500]">Agent</span>
                        <Tooltip
                          title={
                            <span className="font-[Montserrat]">
                              {tooltips['Agent']}
                            </span>
                          }
                          className="w-5 absolute left-[4rem] top-[2px] z-[999]"
                          placement="bottom"
                        >
                          <HelpOutlineOutlined />
                        </Tooltip>
                        <div className="absolute left-[10rem] top-[-4px]">
                          <AgentSelect />
                        </div>
                      </div>
                      <div className="flex relative z-[999]">
                        <span className="font-[500]">Plugins</span>
                        <Tooltip
                          title={
                            <span className="font-[Montserrat]">
                              {tooltips['Plugins']}
                            </span>
                          }
                          className="font-[Montserrat] w-5 absolute left-[4.8rem] top-[2px] z-[999]"
                          placement="bottom"
                        >
                          <HelpOutlineOutlined />
                        </Tooltip>
                        {selectedConversation.agent.id == 'plugins-agent' && (
                          <div className="absolute left-[10rem] top-[-4px]">
                            <PluginSelect />
                          </div>
                        )}
                        {selectedConversation.agent.id ==
                          'data-agent' && (
                          <div className="absolute left-[10rem] top-[-4px]">
                            <CodeInterpreterPluginSelect />
                          </div>
                        )}
                        {selectedConversation.agent.id == 'web-agent' && (
                          <div className="absolute left-[10rem]">
                            Please follow the instructions{' '}
                            <a
                              className="underline"
                              target="_blank"
                              href="https://docs.xlang.ai/user-manual/web-agent-setup"
                            >
                              here
                            </a>{' '}
                            to use the Web Agent.
                          </div>
                        )}
                      </div>
                      <div className="flex relative pt-[11rem] w-[45rem]">
                        <span className="font-[500]">Temperature</span>
                        <Tooltip
                          title={
                            <span className="font-[Montserrat]">
                              {tooltips['Temperature']}
                            </span>
                          }
                          className="font-[Montserrat] w-5 absolute left-[8rem] top-[11.2rem] z-[999]"
                          placement="bottom"
                        >
                          <HelpOutlineOutlined />
                        </Tooltip>
                        <TemperatureSlider
                          onChangeTemperature={(temperature) =>
                            handleUpdateConversation(
                              selectedConversation,
                              {
                                key: 'temperature',
                                value: temperature,
                              },
                              false,
                            )
                          }
                        />
                      </div>
                    </Paper>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div className="sticky fixed top-0 h-[3.6rem] leading-[3.6rem] z-10 flex items-center justify-center space-x-20 bg-[#F3F3F3] text-base text-[#666666]">
                  <div>
                    <span className="font-[600]">{t('Agent')}:</span>
                    <span className="ml-2">
                      {selectedConversation?.agent.name}
                    </span>
                  </div>
                  <div>
                    <span className="font-[600]">{t('Base LLM')}:</span>
                    <span className="ml-2">
                      {selectedConversation?.agent?.llm?.name}
                    </span>
                  </div>
                  <div className="flex items-center justify-center">
                    <span className="font-[600]">{t('Enabled Plugins')}:</span>
                    <div className="ml-2 flex space-x-1">
                      {selectedConversation?.agent.id == 'data-agent' &&
                        selectedConversation.selectedCodeInterpreterPlugins.map(
                          (plugin) =>
                            plugin.icon ? (
                              <img
                                className="h-6"
                                src={plugin.icon}
                                alt={plugin.nameForHuman}
                              />
                            ) : (
                              <ExtensionOutlinedIcon className="h-6" />
                            ),
                        )}
                      {selectedConversation?.agent.id == 'plugins-agent' &&
                        selectedConversation.selectedPlugins.map((plugin) =>
                          plugin.icon ? (
                            <img
                              className="h-6"
                              src={plugin.icon}
                              alt={plugin.nameForHuman}
                            />
                          ) : (
                            <ExtensionOutlinedIcon className="h-6" />
                          ),
                        )}
                    </div>
                  </div>
                </div>

                {showSettings && (
                  <SettingsModal setIsSettingsModalOpen={setShowSettings} />
                )}

                {selectedConversation?.messages.map((message, index) => (
                  <ChatMessage
                    key={index}
                    message={message}
                    messageIndex={index}
                    onEdit={(editedMessage) => {
                      setCurrentMessage(editedMessage);
                      // discard edited message and the ones that come after then resend
                      handleSend(
                        editedMessage,
                        selectedConversation?.messages.length - index,
                      );
                      if (isStreamingError) setShowInputBox(false);
                      if (isStopMessageStreaming && isStopChatID == chat_id) {
                        homeDispatch({
                          field: 'isStopMessageStreaming',
                          value: false,
                        });
                        homeDispatch({ field: 'isStopChatID', value: '' });
                      }
                    }}
                    onRegenerate={handleRegenerate}
                    scrollToBottom={() => {
                      messagesEndRef.current?.scrollIntoView({
                        behavior: 'smooth',
                      });
                    }}
                  />
                ))}

                {loading && <ChatLoader />}

                {!(isStreamingError && isStreamingErrorChatID == chat_id) &&
                  !followUpLoading &&
                  !messageIsStreaming &&
                  selectedConversation &&
                  selectedConversation.messages.length > 0 &&
                  recommendChatID == chat_id && (
                    <QuestionSuggestion
                      followUpQuestions={followUpQuestions}
                      scrollToBottom={() => {
                        messagesEndRef.current?.scrollIntoView({
                          behavior: 'smooth',
                        });
                      }}
                      onClick={(message) => {
                        setCurrentMessage(message);
                        handleSend(message, 0, false, null);
                      }}
                    />
                  )}

                <div className="h-[162px] bg-[#F3F3F3]" ref={messagesEndRef} />
              </>
            )}
          </div>

          <ChatInput
            textareaRef={textareaRef}
            onSend={(message, plugin) => {
              setCurrentMessage(message);
              handleSend(message, 0, false, plugin);
            }}
            onScrollDownClick={handleScrollDown}
            showScrollDownButton={showScrollDownButton}
            showInputBox={showInputBox}
          />
        </>
      )}
    </div>
  );
});
Chat.displayName = 'Chat';
