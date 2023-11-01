import { Plugin } from '@/types/plugin';

import { OpenAgent } from './agent';

export interface Message {
  id: number | null;
  role: Role;
  content: string;
  type?: MessageType;
  richContent?: RichContent | null;
  apiType?: string | null;
}

export type Role = 'assistant' | 'user';

export type MessageType = 'rich_message' | 'alert_message' | '';

export interface RichContent {
  intermediateSteps: RichContentItem[];
  finalAnswer: RichContentItem[];
}

export interface RichContentItem {
  id: number;
  message_id: number | null;
  content: string;
  type: RichContentItemType;
}

export type RichContentItemType =
  | 'plain'
  | 'tool'
  | 'card_info'
  | 'transition'
  | 'error'
  | 'echarts'
  | 'evaluation_result'
  | 'image'
  | 'table'
  | 'file_upload_result'
  | 'kaggle_connect'
  | 'kaggle_search'
  | 'snowflake_connector'
  | 'html';

export interface ChatBody {
  agent: OpenAgent;
  messages: Message[];
  key: APIKey;
  prompt: string;
  temperature: number;
}

export interface Conversation {
  id: string | null;
  name: string;
  messages: Message[];
  agent: OpenAgent;
  prompt: string;
  temperature: number;
  folderId: string | null;
  bookmarkedMessagesIds?: number[];
  plugins?: string[];
  selectedCodeInterpreterPlugins: Plugin[];
  selectedPlugins: Plugin[];
}

export interface ConversationNameListItem {
  id: string | null;
  name: string;
  folderId: string | null;
}

export interface APIKey {
  openai: string;
  anthropic: string;
}
