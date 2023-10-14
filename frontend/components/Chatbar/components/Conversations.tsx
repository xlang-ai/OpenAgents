import { ConversationNameListItem } from '@/types/chat';

import { ConversationComponent } from './Conversation';

interface Props {
  conversationNameList: ConversationNameListItem[];
}

export const Conversations = ({ conversationNameList }: Props) => {
  return (
    <div className="flex w-full flex-col gap-1 mt-1">
      {conversationNameList
        .filter((conversation) => !conversation.folderId)
        .slice()
        .reverse()
        .map((conversation, index) => (
          <ConversationComponent key={index} conversation={conversation} />
        ))}
    </div>
  );
};
