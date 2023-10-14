import { ConversationNameListItem } from '@/types/chat';
import { FileItem } from '@/types/files';

export interface ChatbarInitialState {
  searchTerm: string;
  fileSearchTerm: string;
  filteredConversations: ConversationNameListItem[];
  filteredFiles: FileItem[];
}

export const initialState: ChatbarInitialState = {
  searchTerm: '',
  fileSearchTerm: '',
  filteredConversations: [],
  filteredFiles: [],
};
