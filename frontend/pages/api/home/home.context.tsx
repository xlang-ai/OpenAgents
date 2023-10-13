import { Dispatch, createContext } from 'react';

import { ActionType } from '@/hooks/useCreateReducer';

import { Conversation, ConversationNameListItem, Message } from '@/types/chat';
import { KeyValuePair } from '@/types/data';
import { FileItem } from '@/types/files';
import { FolderType } from '@/types/folder';
import { Plugin } from '@/types/plugin';

import { HomeInitialState } from './home.state';
export interface HomeContextProps {
  state: HomeInitialState;
  dispatch: Dispatch<ActionType<HomeInitialState>>;
  handleNewConversation: () => void;
  handleCreateFolder: (name: string, type: FolderType) => void;
  handleDeleteFolder: (folderId: string) => void;
  handleUpdateFolder: (folderId: string, name: string) => void;
  handleSelectConversation: (conversation: ConversationNameListItem) => void;
  handleUpdateConversation: (
    conversation: Conversation,
    data: KeyValuePair,
    syncToServer: boolean,
  ) => void;
  handleUploadFileToServer: (
    file: File,
    chat_id: string,
  ) => Promise<void>;
  handleFetchDataPath: (chat_id: string, highlighted_files: string[]) => void;
  handleMoveFiles: (chat_id: string, nodes: FileItem[]) => Promise<boolean>;
  handleApplyFileToConversation: (
    chat_id: string,
    selectedNode: FileItem,
  ) => Promise<boolean>;
  handleDownloadFile: (
    selectedNode: FileItem,
  ) => Promise<Blob | undefined>;
  handleFetchData: (
    chat_id: string,
    file_path: string,
  ) => Promise<string>;
  handleFetchDataFlow: (node_list: number[]) => any;
  handleUpdateFile: (
    chat_id: string,
    node: FileItem,
    renameValue: string
  ) => void;
  handleDeleteFile: (chat_id: string, node: FileItem) => void;
  handleSend: (
    message: Message,
    deleteCount?: number,
    isEdited?: boolean,
    plugin?: Plugin | null,
    apiCall?: any,
    isRegenerate?: boolean,
  ) => Promise<void>;
}

const HomeContext = createContext<HomeContextProps>(undefined!);

export default HomeContext;
