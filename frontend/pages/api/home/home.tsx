import { useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';
import 'react-reflex/styles.css';
import { GetServerSideProps } from 'next';
import { useTranslation } from 'next-i18next';
import { serverSideTranslations } from 'next-i18next/serverSideTranslations';
import Head from 'next/head';
import { useCreateReducer } from '@/hooks/useCreateReducer';
import { FileItem } from '@/types/files'
import { Plugin } from '@/types/plugin';
import autoIconURL from '@/public/auto_icon_base64';


import {
  cleanSelectedConversation,
} from '@/utils/app/clean';
import {
  API_GET_DATA,
  API_REGISTER_FOLDER,
  API_DELETE_FOLDER,
  API_UPDATE_FOLDER,
  API_GET_PATH_TREE,
  API_GET_TOOL_LIST,
  API_APPLY_FILE_TO_CONVERSATION,
  API_UPLOAD,
  API_UPDATE_FILE,
  API_DELETE_FILE,
  DEFAULT_SYSTEM_PROMPT,
  DEFAULT_TEMPERATURE,
  API_GET_FOLDER_LIST,
  API_MOVE_FILES,
  API_GET_LLM_LIST,
  API_DOWNLOAD_FILE,
  API_GET_DATA_TOOL_LIST,
} from '@/utils/app/const';
import { API_GET_DATAFLOW } from '@/utils/app/const';
import {
  getConversation,
  getConversationNameList,
  updateConversationNameList,
} from '@/utils/app/conversation';
import { saveFolders } from '@/utils/app/folders';
import {registerConversation} from '@/utils/app/conversation';

import {
  ChatBody,
  Conversation,
  ConversationNameListItem,
  Message,
  RichContent,
} from '@/types/chat';
import { KeyValuePair } from '@/types/data';
import { FolderInterface, FolderType } from '@/types/folder';
import { LLM, OpenAgentID, OpenAgents, fallbackModelID } from '@/types/agent';

import { Navbar } from '@/components/Mobile/Navbar';

import HomeContext from './home.context';
import { HomeInitialState, initialState } from './home.state';

import { v4 as uuidv4 } from 'uuid';
import { getEndpoint, getRecommendationEndpoint } from '@/utils/app/api';
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { Chatbar } from '@/components/Chatbar/Chatbar';
import { Chat } from '@/components/Chat/Chat';

interface Props {
  serverSideApiKeyIsSet: boolean;
  serverSidePluginKeysSet: boolean;
  defaultAgentId: OpenAgentID;
}

const Home = ({
  serverSideApiKeyIsSet,
  serverSidePluginKeysSet,
  defaultAgentId,
}: Props) => {
  const { t } = useTranslation('chat');
  const [selectedNode, setSelectedNode] = useState<FileItem | undefined>(undefined);

  const contextValue = useCreateReducer<HomeInitialState>({
    initialState,
  });

  const {
    state: {
      chat_id,
      apiKey,
      lightMode,
      folders,
      conversationNameList,
      selectedConversation,
      apiKeyUploading,
      selectedPlugins,
      pluginKeys,
      isCreateNewConversation,
      isStopMessageStreaming,
      isStreamingError,
      defaultSelectedCodeInterpreterPlugins,
      agents,
      cachedConversations,
      defaultLLMId,
      showTerms,
    },
    dispatch,
  } = contextValue;

  const stopConversationRef = useRef<boolean>(false);


  const handleSend = async (
      message: Message,
      deleteCount = 0,
      isEdited = false,
      plugin: Plugin | null = null,
      apiCall: any | null = null,
      isRegenerate = false,
    ) => {
      if (selectedConversation) {
        let updatedConversation: Conversation;
        if (deleteCount) {
          // TODO: Need to handle delete count logic for API calls
          const updatedMessages = [...selectedConversation.messages];
          for (let i = 0; i < deleteCount; i++) {
            updatedMessages.pop();
          }
          updatedConversation = {
            ...selectedConversation,
            messages: [...updatedMessages, message],
          };
        } else {
          if (apiCall) {
            updatedConversation = selectedConversation
          } else {
            updatedConversation = {
              ...selectedConversation,
              messages: [...selectedConversation.messages, message],
            };
          }
        }

        dispatch({
          field: 'selectedConversation',
          value: updatedConversation,
        });
        dispatch({
          field: 'isStreamingMessageId',
          value: updatedConversation.messages.length,
        });
        dispatch({ field: 'loading', value: true });
        dispatch({ field: 'messageIsStreaming', value: true });
        const chatBody: ChatBody = {
          agent: updatedConversation.agent,
          key: apiKey,
          messages: updatedConversation.messages,
          prompt: updatedConversation.prompt,
          temperature: updatedConversation.temperature,
        };

        dispatch({ field: 'followUpLoading', value: true });

        let isNewConversation = true;

        const newConversation: Conversation = {
          id: null,
          name: t('New Conversation'),
          messages: [],
          agent: OpenAgents[defaultAgentId],
          prompt: DEFAULT_SYSTEM_PROMPT,
          temperature: DEFAULT_TEMPERATURE,
          folderId: null,
          selectedCodeInterpreterPlugins: defaultSelectedCodeInterpreterPlugins,
          selectedPlugins: []
        };

        if ((apiCall && updatedConversation.messages.length === 0) 
            || ((! apiCall) && updatedConversation.messages.length === 1)) {
            if (isCreateNewConversation) {
              // create by clicking "New Conversation"
              updatedConversation.id = selectedConversation.id;
              dispatch({ field: 'isCreateNewConversation', value: false });
            }
            // create by clicking "Send"
            if (!isStreamingError) {
              let data;
              try {
                data = await registerConversation(updatedConversation);
              } catch(error) {
                toast.error((error as Error).message);
                dispatch({ field: 'chat_id', value: '' });
                dispatch({ field: 'selectedConversation', value: newConversation });
                dispatch({ field: 'loading', value: false });
                dispatch({ field: 'messageIsStreaming', value: false });
                return;
              }
              updatedConversation.id = data.id;
              dispatch({ field: 'chat_id', value: data.id });
            }
        }

        const endpoint = getEndpoint(chatBody.agent);
        let body;
        let user_intent = ""
        let parent_message_id: number | null = -1;
        if (!plugin) {
          if (apiCall || message.apiType == 'DataProfiling') {
            // Did not input message into conversation
            if (chatBody.messages.length > 0) {
              parent_message_id =
                chatBody.messages[chatBody.messages.length - 1].id;
            }
          } else {
            // Append input message into conversation
            if (chatBody.messages.length > 1) {
              parent_message_id =
                chatBody.messages[chatBody.messages.length - 2].id;
            }
            user_intent = chatBody.messages[chatBody.messages.length - 1].content
          }
          body = JSON.stringify({
            user_intent: message.apiType == 'DataProfiling' ? '' : user_intent,
            chat_id: updatedConversation.id,
            parent_message_id: parent_message_id,
            selected_plugins: selectedPlugins.map((plugin) => plugin.id),
            code_interpreter_languages: selectedConversation.selectedCodeInterpreterPlugins.filter((plugin) => plugin.type === "language"),
            code_interpreter_tools: selectedConversation.selectedCodeInterpreterPlugins.filter((plugin) => plugin.type === "tool"),
            // TODO: need to handle other possible api calls in the future
            api_call: message.apiType == 'DataProfiling' ? {
              api_name: "DataProfiling",
              args: {
                activated_file: selectedNode,
                chat_id: selectedConversation.id,
                parent_message_id: parent_message_id
              }} : apiCall,
            is_regenerate: isRegenerate,
            llm_name: updatedConversation.agent?.llm?.name,
            temperature: updatedConversation.temperature,
            api_key: apiKey,
          });
        } else {
          body = JSON.stringify({
            ...chatBody,
            googleAPIKey: pluginKeys
              .find((key) => key.pluginId === 'google-search')
              ?.requiredKeys.find((key) => key.key === 'GOOGLE_API_KEY')?.value,
            googleCSEId: pluginKeys
              .find((key) => key.pluginId === 'google-search')
              ?.requiredKeys.find((key) => key.key === 'GOOGLE_CSE_ID')?.value,
          });
        }
        const controller = new AbortController();
        let response;
        try {
          response = await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            signal: controller.signal,
            body,
          });
        } catch (error: unknown) {
          toast.error((error as Error).message);
          dispatch({ field: 'loading', value: false });
          dispatch({ field: 'messageIsStreaming', value: false });
          dispatch({ field: 'selectedConversation', value: newConversation });
          return;
        }
        if (!response.ok) {
          dispatch({ field: 'loading', value: false });
          dispatch({ field: 'messageIsStreaming', value: false });
          dispatch({ field: 'selectedConversation', value: newConversation });
          toast.error(response.statusText);
          return;
        }
        const data = response.body;
        if (!data) {
          dispatch({ field: 'loading', value: false });
          dispatch({ field: 'messageIsStreaming', value: false });
          dispatch({ field: 'selectedConversation', value: newConversation });
          toast.error('Error streaming message!');
          return;
        }

        if (!plugin) {
          if (updatedConversation.messages.length === 1) {
            const { content } = message;
            let customName = content;
            if (message.apiType == 'DataProfiling' && selectedNode) {
              customName = selectedNode.text;
            }
            updatedConversation = {
              ...updatedConversation,
              name: customName,
            };
            if (!isStreamingError) {
              (async () => {
                const convs: ConversationNameListItem[] = [{
                  id: updatedConversation.id,
                  name: updatedConversation.name,
                  folderId: updatedConversation.folderId,
                }]
                try {
                  await updateConversationNameList(convs);
                } catch (error) {
                  toast.error((error as Error).message);
                  dispatch({ field: 'loading', value: false });
                  dispatch({ field: 'messageIsStreaming', value: false });
                  dispatch({ field: 'selectedConversation', value: newConversation });
                  return;
                }
              })();
            }
          }
          const reader = data.getReader();
          const decoder = new TextDecoder();
          let done = false;
          let isFirst = true;
          let richContent: RichContent = {
            intermediateSteps: [],
            finalAnswer: [],
          };

          let richMessage: Message = {
            id: null,
            role: 'assistant',
            type: 'rich_message',
            content: '',
            richContent: null,
          };

          let concatIntermediateStepText = '';
          let concatFinalAnswerText = '';
          let finalAnswerText = ''

          let stream_buffer: number[] = [];
          let json_size = -1;

          let aiMessageId: number | null = null;
          let humanMessageId: number | null = null;

          let isError = false;

          while (!done) {
            if (stopConversationRef.current === true) {
              controller.abort();
              done = true;
              stopConversationRef.current = false;
              // break;
            }

            const { value, done: doneReading } = await reader.read();
            if (stream_buffer.length === 0 && value === undefined) {
              break;
            }
            if (value !== undefined) {
              value.forEach((element) => {
                stream_buffer.push(element);
              });
            }

            // We need read the first 4 bytes to get the size of the json
            while (true) {
              if (json_size === -1) {
                // We need to read more bytes to get the size of the json
                if (stream_buffer.length < 4) {
                  break;
                } else {
                  let buffer = new ArrayBuffer(4);
                  let byteArray = new Uint8Array(buffer);
                  for (let i = 0; i < 4; i++) {
                    byteArray[i] = stream_buffer[i];
                  }
                  let dataView = new DataView(buffer);
                  json_size = dataView.getInt32(0, true);
                  stream_buffer = stream_buffer.slice(4);
                  continue;
                }
              }
              // We need to read the json, but json is not complete now
              else if (stream_buffer.length < json_size) {
                break;
              }
              // We have complete json now

              const chunkValue = decoder.decode(
                new Uint8Array(stream_buffer.slice(0, json_size)),
              );
              stream_buffer = stream_buffer.slice(json_size);
              json_size = -1;

              let chunkValueJson = JSON.parse(chunkValue);
              if (chunkValueJson?.intermediate_steps?.type == 'heartbeat') {
                continue;
              }

              if (chat_id in chunkValueJson && chunkValueJson['chat_id'] != updatedConversation.id) {
                console.log(chunkValueJson, updatedConversation.id)
                continue;
              }

              if ('success' in chunkValueJson && 'error' in chunkValueJson) {
                let newAlertMessage : Message = {
                  id: null,
                  role: 'assistant',
                  type: 'alert_message',
                  content: '',
                  richContent: null,
                };
                switch (chunkValueJson['error']) {
                  case 'stop':
                    // newAlertMessage.content = 'Stopped generation.';
                    newAlertMessage = richMessage;
                    controller.abort();
                    dispatch({ field: 'isStopMessageStreaming', value: true });
                    dispatch({ field: 'isStopChatID', value: chat_id });
                    break;
                  case 'timeout':
                    newAlertMessage.content = 'Timeout. Please try again later.';
                    break;
                  case 'internal':
                    if ('error_msg' in chunkValueJson) newAlertMessage.content = chunkValueJson['error_msg'];
                    else newAlertMessage.content = 'Server internal error. Please try again later.';
                    break;
                }
                let newConversation : Conversation;
                let newMessages : Message[] = updatedConversation.messages;
                if (newMessages.length == 0) {
                  // the current user message has not been stored in selectedConversation
                  newMessages.push(message);
                } else {
                  // if using data summary, we sent a dummy message to the server
                  // selectedConversation has a user message containing table info
                  if (newMessages[newMessages.length - 1].apiType != 'DataProfiling') {
                    // if not, no dummy message, so replace
                    // if ai message is already partly inserted (in case of timeout), don't replace
                    if (newMessages[newMessages.length - 1].id == message.id) {
                      newMessages[newMessages.length - 1] = message;
                    }
                  }
                }
                if (newMessages[newMessages.length - 1].role == 'assistant') {
                  newMessages[newMessages.length - 1] = newAlertMessage;
                } else {
                  newMessages.push(newAlertMessage);
                }
                newConversation = {
                  ...selectedConversation,
                  messages: newMessages,
                }
                dispatch({ field: 'selectedConversation', value: newConversation });
                dispatch({ field: 'isStreamingError', value: true });
                dispatch({ field: 'isStreamingErrorChatID', value: chat_id });
                done = true;
                isError = true;
                break;
              }
              
              if (
                'ai_message_id' in chunkValueJson &&
                'human_message_id' in chunkValueJson
              ) {
                aiMessageId = chunkValueJson['ai_message_id'];
                humanMessageId = chunkValueJson['human_message_id'];
                if (humanMessageId) {
                  updatedConversation.messages[
                    updatedConversation.messages.length - 1
                  ].id = chunkValueJson['human_message_id'];
                }
              } else {
                // Block-level Streaming Method
                if (
                  !('streaming_method' in chunkValueJson) ||
                  chunkValueJson['streaming_method'] === 'block'
                ) {
                  if (chunkValueJson['intermediate_steps']) {
                    const updatedIntermediateSteps = [
                      ...richContent.intermediateSteps,
                      ...chunkValueJson['intermediate_steps']?.map(
                        (
                          step_content: {
                            type: string;
                            text: string;
                            id: string;
                          },
                          index: number,
                        ) => {
                          return {
                            id: step_content.id,
                            message_id: aiMessageId,
                            content: step_content.text,
                            type: step_content.type,
                          };
                        },
                      ),
                    ];
                    richContent.intermediateSteps = updatedIntermediateSteps;
                  }
                  if (chunkValueJson['final_answer']) {
                    const updatedFinalAnswer = [
                      ...richContent.finalAnswer,
                      ...chunkValueJson['final_answer']?.map(
                        (
                          step_content: {
                            type: string;
                            text: string;
                            id: string;
                          },
                          index: number,
                        ) => {
                          return {
                            id: step_content.id,
                            message_id: aiMessageId,
                            content: step_content.text,
                            type: step_content.type,
                          };
                        },
                      ),
                    ];
                    richContent.finalAnswer = updatedFinalAnswer;
                  }
                  richMessage = {
                    id: aiMessageId,
                    role: 'assistant',
                    type: 'rich_message',
                    content: '',
                    richContent: richContent,
                  };
                } else if (chunkValueJson['streaming_method'] === 'card_info'){
                  if (chunkValueJson['final_answer']) {
                    const content = chunkValueJson['final_answer'];
                    finalAnswerText = content.text;
                    const updatedFinalAnswer = [
                        ...richContent.finalAnswer,
                        {
                          id: content.id,
                          message_id: aiMessageId,
                          content: finalAnswerText,
                          type: content.type,
                        },
                      ];
                    richContent.finalAnswer = updatedFinalAnswer;
                  }
                  richMessage = {
                    id: aiMessageId,
                    role: 'assistant',
                    type: 'rich_message',
                    content: '',
                    richContent: richContent,
                  };
                } else {
                  // char
                  if (chunkValueJson['is_block_first']) {
                    if (chunkValueJson['intermediate_steps']) {
                      const step_content = chunkValueJson['intermediate_steps'];
                      concatIntermediateStepText = step_content.text;
                      const updatedIntermediateSteps = [
                        ...richContent.intermediateSteps,
                        {
                          id: step_content.id,
                          message_id: aiMessageId,
                          content: concatIntermediateStepText,
                          type: step_content.type,
                        },
                      ];
                      richContent.intermediateSteps = updatedIntermediateSteps;
                    }
                    if (chunkValueJson['final_answer']) {
                      const step_content = chunkValueJson['final_answer'];
                      concatFinalAnswerText = step_content.text;
                      const updatedFinalAnswer = [
                        ...richContent.finalAnswer,
                        {
                          id: step_content.id,
                          message_id: aiMessageId,
                          content: concatFinalAnswerText,
                          type: step_content.type,
                        },
                      ];
                      richContent.finalAnswer = updatedFinalAnswer;
                    }
                  } else {
                    if (chunkValueJson['intermediate_steps']) {
                      const step_content = chunkValueJson['intermediate_steps'];
                      concatIntermediateStepText += step_content.text;
                      const updatedIntermediateSteps =
                        richContent.intermediateSteps.map((step, index) => {
                          if (
                            index ===
                            richContent.intermediateSteps.length - 1
                          ) {
                            return {
                              ...step,
                              content: concatIntermediateStepText,
                            };
                          }
                          return step;
                        });
                      richContent.intermediateSteps = updatedIntermediateSteps;
                    }
                    if (chunkValueJson['final_answer']) {
                      const step_content = chunkValueJson['final_answer'];
                      concatFinalAnswerText += step_content.text;
                      let updatedFinalAnswer
                      updatedFinalAnswer = richContent.finalAnswer.map(
                          (step, index) => {
                            if (index === richContent.finalAnswer.length - 1) {
                              return {
                                ...step,
                                content: concatFinalAnswerText,
                              };
                            }
                            return step;
                          },
                        );
                      richContent.finalAnswer = updatedFinalAnswer
                      }
                    }
                  
                  richMessage = {
                    id: aiMessageId,
                    role: 'assistant',
                    type: 'rich_message',
                    content: '',
                    richContent: richContent,
                  };
                }
              } // End of ai_message_id and human_message_id check
              if (
                !(
                  'ai_message_id' in chunkValueJson &&
                  'human_message_id' in chunkValueJson
                )
              ) {
                if (isFirst) {
                  isFirst = false;
                  richMessage.id = aiMessageId;
                  const updatedMessages: Message[] = [
                    ...updatedConversation.messages,
                    richMessage,
                  ];
                  updatedConversation = {
                    ...updatedConversation,
                    messages: updatedMessages,
                  };

                  dispatch({ field: 'loading', value: false });
                  dispatch({
                    field: 'selectedConversation',
                    value: updatedConversation,
                  });
                } else {
                  const updatedMessages: Message[] =
                    updatedConversation.messages.map((message, index) => {
                      if (index === updatedConversation.messages.length - 1) {
                        return {
                          ...message,
                          richContent: richContent,
                        };
                      }
                      return message;
                    });

                  updatedConversation = {
                    ...updatedConversation,
                    messages: updatedMessages,
                  };
                  dispatch({
                    field: 'selectedConversation',
                    value: updatedConversation,
                  });
                }
              } // End of ai_message_id and human_message_id check
            }

            // No more content in buffer and no new data, we are done
            if (stream_buffer.length === 0 && doneReading) break;
          }

          const updatedConversationNameList: ConversationNameListItem[] = conversationNameList.map(
            (conversation) => {
              if (conversation.id === selectedConversation.id) {
                isNewConversation = false
                return {
                  id: updatedConversation.id,
                  folderId: null,
                  name: updatedConversation.name,
                };
              }
              return conversation;
            },
          );
          
          if (isNewConversation) {
            if (updatedConversation.id && 
              !updatedConversationNameList.find((c) => c.id === updatedConversation.id)) {
              updatedConversationNameList.push({
                id: updatedConversation.id,
                folderId: null,
                name: updatedConversation.name,
              });
            }
          }

          if (!isError) {
            dispatch({ field: 'isStreamingError', value: false });
            dispatch({ field: 'isStreamingErrorChatID', value: '' });
            if (isStopMessageStreaming) {
              dispatch({ field: 'isStopMessageStreaming', value: false });
              dispatch({ field: 'isStopChatID', value: '' });
            }
          }
          dispatch({
            field: 'conversationNameList',
            value: updatedConversationNameList,
          });
          dispatch({ field: 'messageIsStreaming', value: false });
          dispatch({ field: 'loading', value: false });

          if (!isError) {
            // update follow up questions
            if (message.apiType != 'DataProfiling') {
              try {
                const qEndpoint = getRecommendationEndpoint();
                const body = JSON.stringify({
                  user_intent: message.content,
                  chat_id: updatedConversation.id,
                  llm_name: updatedConversation?.agent?.llm?.name,
                  temperature: updatedConversation?.temperature,
                  parent_message_id: parent_message_id,
                  api_key: apiKey,
                });
  
                dispatch({ field: 'followUpLoading', value: true });
  
                const qResponse = await fetch(qEndpoint, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                  },
                  body,
                });
  
                if (!qResponse.ok) {
                  dispatch({ field: 'followUpLoading', value: true });
                }
                dispatch({ field: 'followUpLoading', value: false });
  
                const data = await qResponse.json();
  
                if (!data) {
                  dispatch({ field: 'followUpQuestions', value: [] });
                } else {
                  const updatedQStrings = data.recommend_questions;
                  dispatch({
                    field: 'followUpQuestions',
                    value: updatedQStrings,
                  });
                  dispatch({ field: 'recommendChatID', value: data.chat_id });
                }
              } catch (error) {
                toast.error((error as Error).message);
                dispatch({ field: 'followUpQuestions', value: [] });
                dispatch({ field: 'loading', value: false });
                dispatch({ field: 'messageIsStreaming', value: false });
                dispatch({ field: 'selectedConversation', value: newConversation });
                return;
              }
            }
          }
        }
      }
    };



  const handleSelectConversation = async (
    conversationNameListItem: ConversationNameListItem,
  ) => {
    let conversation: Conversation | undefined;
    if (cachedConversations.has(conversationNameListItem.id)) {
      conversation = cachedConversations.get(conversationNameListItem.id);
      cachedConversations.delete(conversationNameListItem.id);
      cachedConversations.set(conversationNameListItem.id, conversation);
    } else {
      try {
        conversation = await getConversation(
          conversationNameListItem.id,
        );
      } catch (error) {
        toast.error((error as Error).message);
        return;
      }
    }

    dispatch({ field: 'selectedConversation', value: conversation });
    dispatch({ field: 'selectedPlugins', value: conversation?.selectedPlugins });
    dispatch({ field: 'selectedCodeInterpreterPlugins', value: conversation?.selectedCodeInterpreterPlugins});
  };

  // FOLDER OPERATIONS  --------------------------------------------

  const handleCreateFolder = async (name: string, type: FolderType) => {
    const newFolder: FolderInterface = {
      id: uuidv4(),
      name,
      type,
    };
    let response;
    try {
      response = await fetch(API_REGISTER_FOLDER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          folder: newFolder,
        })
      });
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }
    if (!response.ok) {
      toast.error(response.statusText);
      return;
    }
    
    const data = await response.json()
    if (!data || data["success"] === false) {
      toast.error('Error creating folder!');
      return;
    }
    newFolder.id = data["id"]
    const updatedFolders = [...folders, newFolder];
    dispatch({ field: 'folders', value: updatedFolders });
    saveFolders(updatedFolders);
  };

  const handleDeleteFolder = async (folderId: string) => {
    const updatedFolders = folders.filter((f) => f.id !== folderId);

    let response;
    try {
      response = await fetch(API_DELETE_FOLDER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          folder_id: folderId,
        })
      });
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }
    if (!response.ok) {
      toast.error(response.statusText);
      return;
    }
    
    const data = await response.json()
    if (!data || data["success"] === false) {
      toast.error('Error deleting folder!');
      return;
    }

    dispatch({ field: 'folders', value: updatedFolders });
    saveFolders(updatedFolders);

    if (data["success"]) {
      toast.success("Folder deleted!")
    }

    const conversationsToUpdate: ConversationNameListItem[] = [];
    const updatedConversationNameList = conversationNameList.map((c) => {
      if (c.folderId === folderId) {
        const temp: ConversationNameListItem = { ...c, folderId: null };
        conversationsToUpdate.push(temp);
        return temp;
      }
      return c;
    });

    // update local storage
    dispatch({
      field: 'conversationNameList',
      value: updatedConversationNameList,
    });

    // update the backend
    try {
      updateConversationNameList(conversationsToUpdate);
    } catch (error) {
      toast.error((error as Error).message);
      return;
    }
  };

  const handleUpdateFolder = async (folderId: string, name: string) => {
    const updatedFolders = folders.map((f) => {
      if (f.id === folderId) {
        return {
          ...f,
          name,
        };
      }

      return f;
    });

    let response;
    try {
      response = await fetch(API_UPDATE_FOLDER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          folder_id: folderId,
          name: name,
        })
      });
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }
    if (!response.ok) {
      toast.error(response.statusText);
      return;
    }
    
    const data = await response.json()
    if (!data || data["success"] === false) {
      toast.error("Error updating folder!");
      return;
    }

    dispatch({ field: 'folders', value: updatedFolders });

    saveFolders(updatedFolders);
  };

  // CONVERSATION OPERATIONS  --------------------------------------------

  const handleNewConversation = async () => {
    const newConversation: Conversation = {
      id: null,
      name: t('New Conversation'),
      messages: [],
      agent: {
        id: OpenAgents[defaultAgentId].id,
        name: OpenAgents[defaultAgentId].name,
        maxLength: OpenAgents[defaultAgentId].maxLength,
        tokenLimit: OpenAgents[defaultAgentId].tokenLimit,
        llm: OpenAgents[defaultAgentId].llm,
      },
      prompt: DEFAULT_SYSTEM_PROMPT,
      temperature: selectedConversation?.temperature ?? DEFAULT_TEMPERATURE,
      folderId: null,
      selectedCodeInterpreterPlugins: defaultSelectedCodeInterpreterPlugins,
      selectedPlugins: []
    };

    let data;
    try {
      data = await registerConversation(newConversation);
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }
    newConversation.id = data.id;
    // restore selected tools and plugins
    dispatch({ field: 'selectedPlugins', value: [] });
    dispatch({ field: 'selectedCodeInterpreterPlugins', value: defaultSelectedCodeInterpreterPlugins });
    dispatch({ field: 'pluginsIsSelected', value: {} });
    dispatch({ field: 'codeInterpreterPluginsIsSelected', value: {
      "0c135359-af7e-473b-8425-1393d2943b57": true,   // python
      "8f8e8dbc-ae5b-4950-9f4f-7f5238978806": true,   // data profiling
    } });

    const updatedConversationNameList: ConversationNameListItem[] = JSON.parse(
      JSON.stringify(conversationNameList),
    );

    updatedConversationNameList.push({
      id: newConversation.id,
      folderId: null,
      name: t('New Conversation'),
    });

    dispatch({ field: 'selectedConversation', value: newConversation });
    dispatch({
      field: 'conversationNameList',
      value: updatedConversationNameList,
    });

    // saveConversation(newConversation);

    dispatch({ field: 'loading', value: false });
    dispatch({ field: 'messageIsStreaming', value: false });
    dispatch({ field: 'isCreateNewConversation', value: true });
  };

  const handleUpdateConversation = async (
    conversation: Conversation,
    data: KeyValuePair,
    syncToServer: boolean,
  ) => {

    const updatedConversation = {
      ...conversation,
      [data.key]: data.value,
    };

    // update the conversationNameList
    if (data.key === 'name' || data.key === 'folderId') {
      const conversationsToUpdate: ConversationNameListItem[] = [];
      const updatedConversationNameList = conversationNameList.map((c) => {
        if (c.id === conversation.id) {
          const temp = {
            id: updatedConversation.id,
            folderId: updatedConversation.folderId,
            name: updatedConversation.name,
          };
          conversationsToUpdate.push(temp);
          return temp;
        }
        return c;
      });

      // update local storage
      dispatch({
        field: 'conversationNameList',
        value: updatedConversationNameList,
      });
    }

    // update local storage
    dispatch({ field: 'selectedConversation', value: updatedConversation });
    // update the backend
    if (syncToServer) {
      try {
        await updateConversationNameList([updatedConversation]);
      } catch (error: unknown) {
        toast.error((error as Error).message);
        return;
      }
    }
  };

  const handleUpdateFile = async (
    chat_id: string,
    node: FileItem,
    renameValue: string,
  ) => {
    try {
      const response = await fetch(API_UPDATE_FILE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          chat_id: chat_id,
          node: node,
          rename_value: renameValue
        }),
      });

      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }

      const data = await response.json();
      if (!data) {
        toast.error("Error updating file!")
        return;
      }
      if (data["success"] === false) {
        toast.error(data["message"], {
          style: {
            wordBreak: 'break-all'
          }})
        return;
      }

    } catch (error) {
      toast.error((error as Error).message);
      return;
    }

  }

  const handleDeleteFile = async (
    chat_id: string,
    node: FileItem,
  ) => {
    try {
      const response = await fetch(API_DELETE_FILE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          chat_id: chat_id,
          node: node,
        }),
      });
      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }

      const data = await response.json();
      if (!data) {
        toast.error("Error deleting file!");
        return;
      }
      if (data["success"] === false) {
        toast.error(data["message"], {
          style: {
            wordBreak: 'break-all'
          }})
        return;
      }
      handleFetchDataPath(chat_id, []);
      // console.log(data);

    } catch (error) {
      toast.error((error as Error).message);
      return;
    }

  }

  const handleUploadFileToServer = async (
    file: File,
    chat_id: string,
  ) => {
    return new Promise<void>((resolve, reject) => {
      if (!selectedConversation) return;

      try {
        let parent_id: number | null = -1
        if (selectedConversation.messages.length > 0)
          parent_id = selectedConversation.messages[selectedConversation.messages.length - 1].id
        const formData = new FormData();
        formData.append('file', file);
        formData.append('chat_id', chat_id);
        formData.append('parent_id', String(parent_id))
        formData.append('accessToken', localStorage.getItem('accessToken') || '')

        // console.log(formData.get('file'));

        // Use XMLHttpRequest instead of fetch to track upload progress
        const xhr = new XMLHttpRequest();
        dispatch({ field: 'fileUploadProgress', value: 0 });
        dispatch({ field: 'isFileUpload', value: true });
        dispatch({ field: 'messageIsStreaming', value: true });

        // Event listener for upload progress
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable) {
            const fractionCompleted = event.loaded / event.total;
            dispatch({ field: 'fileUploadProgress', value: fractionCompleted });
          }
        });

          // Event listener for response received
          xhr.addEventListener('load', async () => {
            if (xhr.status == 401) {
              dispatch({ field: 'loading', value: false });
              dispatch({ field: 'messageIsStreaming', value: false });
              dispatch({ field: 'isFileUpload', value: false });
              return;
            }

            // Process the response just fetch's `res.body`
            const data = xhr.response;

          if (!data) {
            dispatch({ field: 'loading', value: false });
            dispatch({ field: 'messageIsStreaming', value: false });
            dispatch({ field: 'isFileUpload', value: false });
            return;
          }

            // Since XMLHttpRequest doesn't return a stream, we create one from the response text
            const responseStream = new ReadableStream({
              start(controller) {
                controller.enqueue(new TextEncoder().encode(data));
                controller.close();
              },
            });

            const reader = responseStream.getReader();
            const decoder = new TextDecoder();

            let updatedConversation: Conversation;
            dispatch({ field: 'loading', value: false });
            const { value, done: doneReading } = await reader.read();
            const chunkValue = decoder.decode(value);

            // Non-streaming Control
            let response;
            try {
              response = JSON.parse(chunkValue);
            } catch (e: any) {
              reject(e);
              return;
            }

          handleFetchDataPath(chat_id, []);

          resolve();
        });

        // Error Handling
        xhr.addEventListener('error', function () {
          const errorMessage =
            'Network error occurred!' +
            {
              status: xhr.status,
              statusText: xhr.statusText,
              readyState: xhr.readyState,
            };
          dispatch({ field: 'isFileUpload', value: false });
          dispatch({ field: 'messageIsStreaming', value: false });
          reject(errorMessage);
        });

        // Start the request
        xhr.open('POST', API_UPLOAD);
        xhr.send(formData);
      } catch (error) {
        dispatch({ field: 'isFileUpload', value: false });
        dispatch({ field: 'messageIsStreaming', value: false });
        reject('Upload failed! ' + error);
      }
    });
  };

  // SETTING UP THE GROUNDING SOURCE
  const handleDownloadFile = async (selectedNode: FileItem) => {
    if (selectedConversation) {
      let body = JSON.stringify({
        chat_id: selectedConversation.id,
        node: selectedNode,
      });
      let response;
      try {
        response = await fetch(API_DOWNLOAD_FILE, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
          body: body,
        });
      } catch (error: unknown) {
        toast.error((error as Error).message);
        return;
      }
      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }
      
      const blob = await response.blob();
      return blob;
    }
  };

  const handleApplyFileToConversation = async (
    chat_id: string,
    selectedNode: FileItem,
  ) => {
    if (selectedConversation) {
      const controller = new AbortController();
      dispatch({ field: 'isSettingGroundingSource', value: true });
      // dispatch({ field: 'messageIsStreaming', value: true });
      let parent_message_id: number | null = -1;
      if (selectedConversation.messages.length === 0) {
        let data;
        try {
          data = await registerConversation(selectedConversation);
        } catch (error: unknown) {
          toast.error((error as Error).message);
        dispatch({ field: 'isSettingGroundingSource', value: false });
          return false;
        }
        selectedConversation.id = data.id;
    }
      if (selectedConversation.messages?.length > 0) {
        parent_message_id =
          selectedConversation.messages[selectedConversation.messages.length - 1].id;
      }
      setSelectedNode(selectedNode);
      let body = JSON.stringify({
        activated_file: selectedNode,
        chat_id: selectedConversation.id,
        parent_message_id: parent_message_id,
      });
      let response;
      try {
        response = await fetch(API_APPLY_FILE_TO_CONVERSATION, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
          signal: controller.signal,
          body: body,
        });
      } catch (error: unknown) {
        toast.error((error as Error).message);
        dispatch({ field: 'isSettingGroundingSource', value: false });
        return false;
      }

      if (!response.ok) {
        dispatch({ field: 'isSettingGroundingSource', value: false });
        toast.error(response.statusText);
        return false;
      }

      const data = await response.json();

      if (!data) {
        toast.error("Error applying file!")
        dispatch({ field: 'isSettingGroundingSource', value: false });
        return false;
      }
      if (data["success"] === false) {
        toast.success(data["message"],
          {
            style: {
              border: '1px solid #713200',
              padding: '16px',
              color: '#713200',
          },
          iconTheme: {
            primary: '#713200',
            secondary: '#FFFAEE',
          }})
        dispatch({ field: 'isSettingGroundingSource', value: false });
        return false;
      }
      let content;
      content = data["content"]

      let fileApplyMessage: Message;

      if (typeof content === 'string') {
        fileApplyMessage = {
          content: content,
          role: 'user',
          type: '',
          id: data["message_id"],
          richContent: null,
          // TODO: need to handle other api calls in the future
          apiType: 'DataProfiling',
        };
      } else {
        fileApplyMessage = {
          content: content,
          role: 'user',
          type: 'rich_message',
          id: data["message_id"],
          richContent: {
            intermediateSteps:
              content['intermediate_steps']?.map(
                (step_content: {
                  type: string;
                  text: string;
                  id: string;
                },
                index: number) => {
                  return {
                    content: step_content.text,
                    type: step_content.type,
                    id: step_content.id,
                    message_id: data["message_id"],
                  }
                }),
            finalAnswer:
              content["final_answer"]?.map(
                (step_content: {
                  type: string;
                  text: string;
                  id: string;
                },
                index: number) => {
                  return {
                    content: step_content.text,
                    type: step_content.type,
                    id: step_content.id,
                    message_id: data["message_id"],
                  }
                }
              )
          },
          // TODO: need to handle other api calls in the future
          apiType: 'DataProfiling',
        };
      }
    
      const updatedMessages: Message[] = [
        ...selectedConversation.messages,
        fileApplyMessage,
      ];

      const updatedConversation = {
        ...selectedConversation,
        messages: updatedMessages,
      };
      dispatch({
        field: 'selectedConversation',
        value: updatedConversation,
      });
      dispatch({ field: 'isSettingGroundingSource', value: false });
      return true;
    }
    return false;
  }

  // EFFECTS  --------------------------------------------

  useEffect(() => {
    if (window.innerWidth < 640) {
      dispatch({ field: 'showChatbar', value: false });
    }
  }, [selectedConversation]);

  useEffect(() => {
    if (!selectedConversation?.id) return;
    if (cachedConversations.has(selectedConversation.id)) {
      cachedConversations.delete(selectedConversation.id);
    } else if (cachedConversations.size >= 5) {
      const firstKey = cachedConversations.keys().next().value;
      cachedConversations.delete(firstKey);
    }
    cachedConversations.set(selectedConversation.id, selectedConversation);
  }, [selectedConversation, selectedConversation?.messages]);

  useEffect(() => {
    defaultAgentId &&
      dispatch({ field: 'defaultAgentId', value: defaultAgentId });
    serverSideApiKeyIsSet &&
      dispatch({
        field: 'serverSideApiKeyIsSet',
        value: serverSideApiKeyIsSet,
      });
    serverSidePluginKeysSet &&
      dispatch({
        field: 'serverSidePluginKeysSet',
        value: serverSidePluginKeysSet,
      });
  }, [defaultAgentId, serverSideApiKeyIsSet, serverSidePluginKeysSet]);

  useEffect(() => {
    // fetch 1st page of conversation name list on load
    (async () => {
      try {
          const conversationNameList = await getConversationNameList(1);
          dispatch({
            field: 'conversationNameList',
            value: conversationNameList,
          });
      } catch (error: unknown) {
        toast.error((error as Error).message);
        return;
      }
    })();
  }, [])

  useEffect(() => {
    const curDate = new Date();
    let expireDate = curDate.setTime(curDate.getTime() + (24 * 60 * 60 * 1000));
    document.cookie = `chat_id=${chat_id}; expires=${expireDate}; path=/`;

    expireDate = curDate.setTime(curDate.getTime() + (30 * 24 * 60 * 60 * 1000));
    const openaiKey = localStorage.getItem('openaiKey') || '';
    const anthropicKey = localStorage.getItem('anthropicKey') || '';
    if (openaiKey) {
      document.cookie = `openaiKey=${openaiKey}; expires=${expireDate}; path=/`
    }
    if (anthropicKey) {
      document.cookie = `anthropicKey=${anthropicKey}; expires=${expireDate}; path=/`;
    }
    dispatch({ field: 'apiKey', value: {
      openai: openaiKey,
      anthropic: anthropicKey,
    } });
  }, [chat_id]);

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch(API_GET_FOLDER_LIST, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          toast.error("Error getting folder list!");
          return;
        }
        const data = await response.json();
        if (!data) {
          toast.error("Error getting folder list!");
          return;
        }
        if (data["success"])
          dispatch({field: 'folders', value: data["data"]});
      } catch (error: unknown) {
        toast.error((error as Error).message);
      }
    })()
  }, [])

  useEffect(() => {
    selectedConversation &&
      dispatch({ field: 'chat_id', value: selectedConversation.id });
  }, [selectedConversation]);

  // ON LOAD --------------------------------------------

  useEffect(() => {
    const apiKey = localStorage.getItem('apiKey');

    if (serverSideApiKeyIsSet) {
      dispatch({ field: 'apiKey', value: '' });

      localStorage.removeItem('apiKey');
    } else if (apiKey) {
      dispatch({ field: 'apiKey', value: apiKey });
    }

    const pluginKeys = localStorage.getItem('pluginKeys');
    if (serverSidePluginKeysSet) {
      dispatch({ field: 'pluginKeys', value: [] });
      localStorage.removeItem('pluginKeys');
    } else if (pluginKeys) {
      dispatch({ field: 'pluginKeys', value: pluginKeys });
    }

    if (window.innerWidth < 640) {
      dispatch({ field: 'showChatbar', value: false });
    }

    const showChatbar = localStorage.getItem('showChatbar');
    if (showChatbar) {
      dispatch({ field: 'showChatbar', value: showChatbar === 'true' });
    }

    const selectedConversation = localStorage.getItem('selectedConversation');
    if (selectedConversation) {
      const parsedSelectedConversation: Conversation =
        JSON.parse(selectedConversation);
      const cleanedSelectedConversation = cleanSelectedConversation(
        parsedSelectedConversation,
      );

      dispatch({
        field: 'selectedConversation',
        value: cleanedSelectedConversation,
      });
    } else {
      (async () => {
        const newConversation: Conversation = {
          id: null,
          name: t('New Conversation'),
          messages: [],
          agent: OpenAgents[defaultAgentId],
          prompt: DEFAULT_SYSTEM_PROMPT,
          temperature: DEFAULT_TEMPERATURE,
          folderId: null,
          selectedCodeInterpreterPlugins: defaultSelectedCodeInterpreterPlugins,
          selectedPlugins: []
        };
        dispatch({
          field: 'selectedConversation',
          value: newConversation,
        });
      })();
    }
  }, [
    defaultAgentId,
    dispatch,
    serverSideApiKeyIsSet,
    serverSidePluginKeysSet,
  ]);

  useEffect(() => {
    const handleGetDataToolList = async () => {
      dispatch({ field: 'codeInterpreterPluginListLoading', value: true });
      let response;
      try {
        response = await fetch(API_GET_DATA_TOOL_LIST, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
      } catch (error: unknown) {
        toast.error((error as Error).message);
      dispatch({ field: 'codeInterpreterPluginListLoading', value: false });
        return;
      }
      
      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }
      const data = await response.json();
      if (!data) {
        toast.error('Error getting data tool list!')
        return;
      }
      let toolList: [Plugin] = data.map(
        (tool: any, index: number) => {
          return {
            id: tool['id'],
            prettyNameForHuman: tool['pretty_name_for_human'],
            nameForHuman: tool['name_for_human'],
            name: tool['name'],
            icon: tool['icon'],
            description: tool['description'],
            type: tool['type']
          };
        },
      );
      const defaultToolIDs = ['PythonCodeBuilder', 'DataProfiling'];
      const defaultToolList = Object.values(toolList).filter((tool: Plugin) => defaultToolIDs.includes(tool.id));
      dispatch({ field: 'selectedCodeInterpreterPlugins', value: defaultToolList });
      dispatch({ field: 'defaultSelectedCodeInterpreterPlugins', value: defaultToolList });
      dispatch({ field: 'codeInterpreterPluginList', value: Object.values(toolList) });
      dispatch({ field: 'codeInterpreterPluginListLoading', value: false });
    }
    const handleGetToolList = async () => {
      dispatch({ field: 'pluginListLoading', value: true });
      const controller = new AbortController();
      let response;
      try {
        response = await fetch(API_GET_TOOL_LIST, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          signal: controller.signal,
        });
      } catch (error: unknown) {
        toast.error((error as Error).message);
      dispatch({ field: 'pluginListLoading', value: false });
        return;
      }
      
      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }
      const data = await response.json();
      if (!data) {
        toast.error('Error getting plugins!');
        return;
      }
      let pluginList: [Plugin] = data.map(
        (plugin: any, index: number) => {
          return {
            id: plugin['id'],
            nameForHuman: plugin['name_for_human'],
            name: plugin['name'],
            // iconId: plugin['iconId'],
            icon: plugin['icon'],
            description: plugin['description'],
            require_api_key: plugin['require_api_key'],
            api_key: plugin['api_key']
          };
        },
      );

      // add auto retrieve plugins
      let newPlugin = {
        id: 'AUTO',
        nameForHuman: 'Auto',
        name: 'auto',
        icon: autoIconURL,
        description: 'Auto select the most suitable plugins for you!',
        require_api_key: false,
        api_key: ""
      };
      // Add the new plugin to the pluginList
      pluginList.unshift(newPlugin);

      dispatch({ field: 'pluginList', value: Object.values(pluginList) });
      dispatch({ field: 'pluginListLoading', value: false });
    };
    handleGetDataToolList();
    handleGetToolList();
  }, [])

  useEffect(() => {
    const handleGetLLMList = async () => {
      let response;
      try {
        response = await fetch(API_GET_LLM_LIST, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
      } catch (error: unknown) {
        toast.error('Error getting LLM list!');
        return;
      }
      
      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }
      const data = await response.json();
      if (!data) {
        toast.error('Error getting LLM list!');
        return;
      }
      const llmList: Record<string, LLM> = data.map((llm: any, index: number) => {
        return {
          id: llm['id'],
          name: llm['name'],
          // TODO: maybe other parameters in the future
        };
      });
      const defaultLLM = Object.values(llmList).find(llm => llm.id == defaultLLMId);
      dispatch({ field: 'llmList', value: Object.values(llmList) });
      dispatch({ field: 'defaultLLM', value: defaultLLM });
      
      // update agents
      agents.forEach(agent => {
        agent.llm = defaultLLM;
      })
    };
    handleGetLLMList();
  }, [apiKeyUploading])

  useEffect(() => {
    localStorage.setItem('chat_id', chat_id);
  }, [chat_id])

  const handleFetchData = async (
    chat_id: string,
    file_path: string,
  ) => {
    try {
      const controller = new AbortController();
      const response = await fetch(API_GET_DATA, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        signal: controller.signal,
        body: JSON.stringify({
          chat_id: chat_id,
          file_path: file_path,
        }),
      });
      const data_ = await response.blob();
      const url = URL.createObjectURL(data_);
      return url;
    } catch (error) {
      console.error(error);
      throw error;
    }
  };

  const handleMoveFiles = async (chat_id: string, nodes: FileItem[]) => {
    // node's parent_id is updated
    try {
      const response = await fetch(API_MOVE_FILES, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          chat_id: chat_id,
          nodes: nodes,
        }),
      });
      if (!response.ok) {
        toast.error(response.statusText);
        return false;
      }

      const data = await response.json();
      if (!data) {
        toast.error("Connection Fails.")
        return false;
      }
      if (data["success"] === false) {
        toast.error(data["message"], {
          style: {
            wordBreak: 'break-all'
          }})
        return false;
      }

    } catch (error: unknown) {
      toast.error((error as Error).message);
      return false;
    }

    return true;
  }

  const handleFetchDataPath = async (chat_id: string, highlighted_files: string[]) => {
    try {
      const controller = new AbortController();
      const response = await fetch(API_GET_PATH_TREE, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        signal: controller.signal,
        body: JSON.stringify({
          chat_id: chat_id,
          highlighted_files: highlighted_files,
        }),
      });
      if (!response.ok) {
        toast.error(response.statusText);
        return;
      }

      const files = await response.json();

      dispatch({ field: 'files', value: files });
    } catch (error) {
      toast.error((error as Error).message);
    }
  };

  const handleFetchDataFlow = async (node_list: number[]) => {
    const response = await fetch(API_GET_DATAFLOW, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        xlangNodes: node_list,
      }),
    });

    const data = response.body;
    if (!data) return;
    const reader = data.getReader();
    const decoder = new TextDecoder();
    const { value, done: doneReading } = await reader.read();
    const chunkValue = decoder.decode(value);
    let chunkValueJson = JSON.parse(chunkValue);

    return chunkValueJson;
  };

  return (
    <HomeContext.Provider
      value={{
        ...contextValue,
        handleNewConversation,
        handleCreateFolder,
        handleDeleteFolder,
        handleUpdateFolder,
        handleSelectConversation,
        handleUpdateConversation,
        handleUploadFileToServer,
        handleFetchDataPath,
        handleMoveFiles,
        handleApplyFileToConversation,
        handleDownloadFile,
        handleFetchData,
        handleFetchDataFlow,
        handleDeleteFile,
        handleUpdateFile,
        handleSend,
      }}
    >
      <Head>
        <title>OpenAgents</title>
        <meta name="description" content="OpenAgents" />
        <meta
          name="viewport"
          content="height=device-height ,width=device-width, initial-scale=1, user-scalable=no"
        />
        <link rel="icon" href="/xlang.ico" />
      </Head>
      {selectedConversation && (
        <main
          className={`flex h-screen w-screen flex-col text-sm text-white ${lightMode} font-[Montserrat] bg-[#F3F3F3]`}
        >
          <Modal
            open={showTerms}
            onClose={() => {dispatch({ field: 'showTerms', value: false })}}
          >
            <div
              className="bg-white p-4 rounded-lg w-fit h-fit absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 overflow-auto"  
            >
                <div className='w-full p-4'>
                  <Typography variant="h4" align='center' className='font-[Montserrat]' gutterBottom>
                    Terms of Use
                  </Typography>
                  <Typography variant="body1" className='font-[Montserrat] mt-5' gutterBottom>
                    By using this chat interface, you accept the following terms and conditions:
                  </Typography>
                  <Typography variant="body1" className='font-[Montserrat] mt-5' gutterBottom>
                    <span className="font-[700]">Generated Information:&nbsp;</span>Please be aware that the information provided by this chat interface, powered by the Language Learning Models (LLM), is generated based on pre-existing data up to a certain cutoff point. As such, it may contain inaccuracies, outdated information, potential toxicity, bias or inconsistencies.
                  </Typography>
                  <Typography variant="body1" className='font-[Montserrat] mt-5' gutterBottom>
                    <span className="font-[700]">Data Collection and Use:&nbsp;</span>Please notice that we collect and store your interactions with this chat interface to help us improve its performance and accuracy. We may use these interactions for evaluation, research, and further training of our models. We always prioritize your privacy and we will make efforts to filter out and remove sensitive and private information from the collected data.
                  </Typography>
                  <Typography variant="body1" className='font-[Montserrat] mt-5' gutterBottom>
                    <span className="font-[700]">Privacy:&nbsp;</span>While we aim to safeguard your privacy, we advise against sharing sensitive personal information such as Social Security numbers, credit card details, and health information. Our team does not have the means to ensure complete security of such data.
                  </Typography>
                  <Typography variant="body1" className='font-[Montserrat] mt-5' gutterBottom>
                    <span className="font-[700]">Performance Limitations:&nbsp;</span>This chat interface is a prototype of our ongoing research preview and is not produced by a professional development team. Consequently, it may have limitations in its performance. We appreciate your understanding and patience as we continue to improve it.
                  </Typography>
                  <Typography variant="body1" className='font-[Montserrat] mt-5' align='right' gutterBottom>
                    XLang Team
                  </Typography>
                </div>
                <IconButton
                  aria-label="close"
                  onClick={() => {dispatch({ field: 'showTerms', value: false })}}
                  className='absolute top-0 right-0'
                >
                  <CloseIcon className='text-3xl' />
                </IconButton>
            </div>
          </Modal>

          <div className="fixed top-0 w-full sm:hidden">
            <Navbar
              selectedConversation={selectedConversation}
              onNewConversation={handleNewConversation}
            />
          </div>

          <div className="flex h-full w-full bg-[#F3F3F3]">
            <Chatbar />
            <div className="flex flex-1 h-full bg-[#F3F3F3]">
              <Chat stopConversationRef={stopConversationRef} />
            </div>
          </div>
          <div id="dialog-root" />
        </main>
      )}
    </HomeContext.Provider>
  );
};
export default Home;

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const defaultAgentId =
    (process.env.DEFAULT_AGENT &&
      Object.values(OpenAgentID).includes(
        process.env.DEFAULT_AGENT as OpenAgentID,
      ) &&
      process.env.DEFAULT_AGENT) ||
    fallbackModelID;

  let serverSidePluginKeysSet = false;

  const googleApiKey = process.env.GOOGLE_API_KEY;
  const googleCSEId = process.env.GOOGLE_CSE_ID;

  if (googleApiKey && googleCSEId) {
    serverSidePluginKeysSet = true;
  }

  return {
    props: {
      serverSideApiKeyIsSet: !!process.env.OPENAI_API_KEY,
      defaultAgentId,
      serverSidePluginKeysSet,
      ...(await serverSideTranslations('en', [
        'common',
        'chat',
        'sidebar',
        'markdown',
        'promptbar',
        'settings',
      ])),
    },
  };
};
