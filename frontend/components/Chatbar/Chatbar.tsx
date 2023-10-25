import { useContext, useEffect } from 'react';
import { toast } from 'react-hot-toast';

import { useTranslation } from 'next-i18next';

import { useCreateReducer } from '@/hooks/useCreateReducer';

import { DEFAULT_SYSTEM_PROMPT, DEFAULT_TEMPERATURE } from '@/utils/app/const';
import {
  clearAllConversations,
  deleteConversation,
  getConversation,
  getConversationNameList,
  saveConversation,
} from '@/utils/app/conversation';
import { exportData } from '@/utils/app/export';
import { saveFolders } from '@/utils/app/folders';

import { Conversation, ConversationNameListItem } from '@/types/chat';
import { OpenAgent, OpenAgents } from '@/types/agent';
import { PluginKey } from '@/types/plugin';

import HomeContext from '@/pages/api/home/home.context';

import { ChatFolders } from './components/ChatFolders';
import { ChatbarSettings } from './components/ChatbarSettings';
import { Conversations } from './components/Conversations';

import Sidebar from '../Sidebar';
import ChatbarContext from './Chatbar.context';
import { ChatbarInitialState, initialState } from './Chatbar.state';

export const Chatbar = () => {
  const { t } = useTranslation('sidebar');

  const chatBarContextValue = useCreateReducer<ChatbarInitialState>({
    initialState,
  });

  const {
    state: {
      showChatbar,
      defaultAgentId,
      folders,
      pluginKeys,
      conversationNameList,
      defaultSelectedCodeInterpreterPlugins,
      files,
    },
    dispatch: homeDispatch,
    handleCreateFolder,
    handleNewConversation,
    handleUpdateConversation,
  } = useContext(HomeContext);

  const {
    state: { searchTerm, filteredConversations, fileSearchTerm },
    dispatch: chatDispatch,
  } = chatBarContextValue;

  const handlePluginKeyChange = (pluginKey: PluginKey) => {
    if (pluginKeys.some((key) => key.pluginId === pluginKey.pluginId)) {
      const updatedPluginKeys = pluginKeys.map((key) => {
        if (key.pluginId === pluginKey.pluginId) {
          return pluginKey;
        }

        return key;
      });

      homeDispatch({ field: 'pluginKeys', value: updatedPluginKeys });

      localStorage.setItem('pluginKeys', JSON.stringify(updatedPluginKeys));
    } else {
      homeDispatch({ field: 'pluginKeys', value: [...pluginKeys, pluginKey] });

      localStorage.setItem(
        'pluginKeys',
        JSON.stringify([...pluginKeys, pluginKey]),
      );
    }
  };

  const handleClearPluginKey = (pluginKey: PluginKey) => {
    const updatedPluginKeys = pluginKeys.filter(
      (key) => key.pluginId !== pluginKey.pluginId,
    );

    if (updatedPluginKeys.length === 0) {
      homeDispatch({ field: 'pluginKeys', value: [] });
      localStorage.removeItem('pluginKeys');
      return;
    }

    homeDispatch({ field: 'pluginKeys', value: updatedPluginKeys });

    localStorage.setItem('pluginKeys', JSON.stringify(updatedPluginKeys));
  };

  const handleExportData = () => {
    exportData();
  };

  const handleClearConversations = async () => {
    try {
      // delete all conversations in the backend
      await clearAllConversations();
      const conversationNameList = await getConversationNameList(1);
      homeDispatch({
        field: 'conversationNameList',
        value: conversationNameList,
      });
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }

    // update local storage
    if (defaultAgentId) {
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
          selectedPlugins: [],
        };
        homeDispatch({
          field: 'selectedConversation',
          value: newConversation,
        });
      })();
    }

    localStorage.removeItem('selectedConversation');

    const updatedFolders = folders.filter((f) => f.type !== 'chat');

    homeDispatch({ field: 'folders', value: updatedFolders });
    saveFolders(updatedFolders);
  };

  const handleDeleteConversation = async (
    conversation: Conversation | ConversationNameListItem,
  ) => {
    try {
      // delete conversation in the backend
      await deleteConversation(conversation);
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }

    // update local storage
    chatDispatch({ field: 'searchTerm', value: '' });

    // update conversationNameList
    const updatedConversationNameList = conversationNameList.filter(
      (c) => c.id !== conversation.id,
    );
    homeDispatch({
      field: 'conversationNameList',
      value: updatedConversationNameList,
    });

    if (updatedConversationNameList.length > 0) {
      try {
        const selectedNewConversation = await getConversation(
          updatedConversationNameList[updatedConversationNameList.length - 1]
            .id,
        );
        homeDispatch({
          field: 'selectedConversation',
          value: selectedNewConversation,
        });
        saveConversation(selectedNewConversation);
      } catch (error: unknown) {
        toast.error((error as Error).message);
        return;
      }
    } else {
      if (defaultAgentId) {
        (async () => {
          const newConversation: Conversation = {
            id: null,
            name: t('New Conversation'),
            messages: [],
            agent: OpenAgents[defaultAgentId],
            prompt: DEFAULT_SYSTEM_PROMPT,
            temperature: DEFAULT_TEMPERATURE,
            folderId: null,
            selectedCodeInterpreterPlugins:
              defaultSelectedCodeInterpreterPlugins,
            selectedPlugins: [],
          };
          homeDispatch({
            field: 'selectedConversation',
            value: newConversation,
          });
        })();
      }
      localStorage.removeItem('selectedConversation');
    }
  };

  const handleToggleChatbar = () => {
    homeDispatch({ field: 'showChatbar', value: !showChatbar });
    localStorage.setItem('showChatbar', JSON.stringify(!showChatbar));
  };

  const handleDrop = async (e: any) => {
    if (e.dataTransfer) {
      let conversation = JSON.parse(e.dataTransfer.getData('conversation'));
      try {
        conversation = await getConversation(conversation.id);
      } catch (error: unknown) {
        toast.error((error as Error).message);
        return;
      }
      handleUpdateConversation(
        conversation,
        { key: 'folderId', value: 0 },
        true,
      );
      chatDispatch({ field: 'searchTerm', value: '' });
      e.target.style.background = '';
    }
  };

  useEffect(() => {
    if (searchTerm) {
      chatDispatch({
        field: 'filteredConversations',
        value: conversationNameList.filter((c) => {
          return c.name.toLowerCase().includes(searchTerm.toLowerCase());
        }),
      });
    } else {
      chatDispatch({
        field: 'filteredConversations',
        value: conversationNameList,
      });
    }
  }, [searchTerm, conversationNameList]);

  useEffect(() => {
    if (fileSearchTerm) {
      chatDispatch({
        field: 'filteredFiles',
        value: files.filter((f) => {
          return f.text.toLowerCase().includes(fileSearchTerm.toLowerCase());
        }),
      });
    } else {
      chatDispatch({
        field: 'filteredFiles',
        value: files,
      });
    }
  }, [fileSearchTerm, files]);

  return (
    <ChatbarContext.Provider
      value={{
        ...chatBarContextValue,
        handleDeleteConversation,
        handleClearConversations,
        handleExportData,
        handlePluginKeyChange,
        handleClearPluginKey,
      }}
    >
      <Sidebar<ConversationNameListItem>
        side={'left'}
        isOpen={showChatbar}
        addItemButtonTitle={t('New Chat')}
        itemComponent={
          <Conversations conversationNameList={filteredConversations} />
        }
        folderComponent={<ChatFolders searchTerm={searchTerm} />}
        items={filteredConversations}
        searchTerm={searchTerm}
        handleSearchTerm={(searchTerm: string) =>
          chatDispatch({ field: 'searchTerm', value: searchTerm })
        }
        toggleOpen={handleToggleChatbar}
        handleCreateItem={handleNewConversation}
        handleCreateFolder={() => handleCreateFolder(t('New folder'), 'chat')}
        handleDrop={handleDrop}
        footerComponent={
          <ChatbarSettings
            searchTerm={fileSearchTerm}
            handleSearchTerm={(fileSearchTerm: string) =>
              chatDispatch({ field: 'fileSearchTerm', value: fileSearchTerm })
            }
          />
        }
      />
    </ChatbarContext.Provider>
  );
};
