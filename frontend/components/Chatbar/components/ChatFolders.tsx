import { useContext } from 'react';
import toast from 'react-hot-toast';

import { getConversation } from '@/utils/app/conversation';

import { FolderInterface } from '@/types/folder';

import HomeContext from '@/pages/api/home/home.context';

import Folder from '@/components/Folder';

import { ConversationComponent } from './Conversation';

interface Props {
  searchTerm: string;
}

export const ChatFolders = ({ searchTerm }: Props) => {
  const {
    state: { folders, conversationNameList },
    handleUpdateConversation,
  } = useContext(HomeContext);

  const handleDrop = async (e: any, folder: FolderInterface) => {
    if (e.dataTransfer) {
      let conversation = JSON.parse(e.dataTransfer.getData('conversation'));
      try {
        conversation = await getConversation(conversation.id);
      } catch (error) {
        toast.error((error as Error).message);
        return;
      }
      handleUpdateConversation(
        conversation,
        {
          key: 'folderId',
          value: folder.id,
        },
        true,
      );
    }
  };

  const ChatFolders = (currentFolder: FolderInterface) => {
    return (
      conversationNameList &&
      conversationNameList
        .filter((conversation) => conversation.folderId)
        .map((conversation, index) => {
          if (conversation.folderId === currentFolder.id) {
            return (
              <div key={index} className="ml-5 pl-1 mt-1">
                <ConversationComponent conversation={conversation} />
              </div>
            );
          }
        })
    );
  };

  return (
    <div className="flex w-full flex-col">
      {folders
        .filter((folder) => folder.type === 'chat')
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((folder, index) => (
          <Folder
            key={index}
            searchTerm={searchTerm}
            currentFolder={folder}
            handleDrop={handleDrop}
            folderComponent={ChatFolders(folder)}
          />
        ))}
    </div>
  );
};
