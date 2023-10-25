import {
  APIKey,
  Conversation,
  ConversationNameListItem,
  Message,
} from '@/types/chat';
import { ErrorMessage } from '@/types/error';
import { ExternalDataFile, FileItem } from '@/types/files';
import { FolderInterface } from '@/types/folder';
import {
  LLM,
  OpenAgentID,
  OpenAgent,
  OpenAgentList,
} from '@/types/agent';
import { PluginKey } from '@/types/plugin';
import { Plugin } from '@/types/plugin';

export interface HomeInitialState {
  apiKey: APIKey;
  pluginKeys: PluginKey[];
  pluginList: Plugin[];
  pluginListLoading: boolean;
  codeInterpreterPluginList: Plugin[];
  codeInterpreterPluginListLoading: boolean;
  loading: boolean;
  lightMode: 'light' | 'dark';
  messageIsStreaming: boolean;
  apiKeyUploading: boolean;
  followUpLoading: boolean;
  modelError: ErrorMessage | null;
  agents: OpenAgent[];
  llmList: LLM[];
  folders: FolderInterface[];
  conversationNameList: ConversationNameListItem[];
  selectedConversation: Conversation | undefined;
  showChatbar: boolean;
  defaultAgentId: OpenAgentID | undefined;
  defaultLLM: LLM | undefined;
  defaultLLMId: string;
  serverSideApiKeyIsSet: boolean;
  serverSidePluginKeysSet: boolean;
  followUpQuestions: string[];
  chat_id: string;
  files: FileItem[];
  fileUploadProgress: number;
  isFileUpload: boolean;
  isSettingGroundingSource: boolean;
  tableIndicesFilter?: number[];
  isStreamingMessageId: number;
  isStopMessageStreaming: boolean;
  isStopChatID: string;
  selectedPlugins: Plugin[];
  selectedCodeInterpreterPlugins: Plugin[];
  defaultSelectedCodeInterpreterPlugins: Plugin[];
  pluginsIsSelected: Partial<Record<string, boolean>>;
  codeInterpreterPluginsIsSelected: Partial<Record<string, boolean>>;
  isCreateNewConversation: boolean;
  isStreamingError: boolean;
  isStreamingErrorChatID: string;
  recommendChatID: string;
  cachedConversations: Map<string | null, Conversation | undefined>;
  showTerms: boolean;
  showAPIKeyModal: boolean;
}

export const initialState: HomeInitialState = {
  apiKey: {
    openai: '',
    anthropic: '',
  },
  loading: false,
  pluginKeys: [],
  pluginList: [],
  pluginListLoading: false,
  codeInterpreterPluginList: [],
  codeInterpreterPluginListLoading: false,
  lightMode: 'dark',
  apiKeyUploading: false,
  messageIsStreaming: false,
  followUpLoading: false,
  modelError: null,
  agents: OpenAgentList,
  llmList: [],
  folders: [],
  conversationNameList: [],
  selectedConversation: undefined,
  showChatbar: true,
  defaultAgentId: undefined,
  defaultLLM: undefined,
  defaultLLMId: 'gpt-3.5-turbo-16k',
  serverSideApiKeyIsSet: false,
  serverSidePluginKeysSet: false,
  followUpQuestions: [],
  chat_id: '',
  files: [{ id: 1, parent: 0, droppable: true, text: 'home' }],
  fileUploadProgress: 0,
  isFileUpload: false,
  isSettingGroundingSource: false,
  isStreamingMessageId: -1,
  isStopMessageStreaming: false,
  isStopChatID: '',
  selectedPlugins: [],
  selectedCodeInterpreterPlugins: [],
  defaultSelectedCodeInterpreterPlugins: [],
  pluginsIsSelected: {},
  codeInterpreterPluginsIsSelected: {
    '0c135359-af7e-473b-8425-1393d2943b57': true, // python
    '8f8e8dbc-ae5b-4950-9f4f-7f5238978806': true, // data profiling
  },
  isCreateNewConversation: false,
  isStreamingError: false,
  isStreamingErrorChatID: '',
  recommendChatID: '',
  cachedConversations: new Map(),
  showTerms: false,
  showAPIKeyModal: false,
};
