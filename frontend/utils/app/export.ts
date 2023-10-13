import { toast } from 'react-hot-toast';
import { getConversation } from './conversation';

export const exportData = async () => {
  const chat_id = localStorage.getItem('chat_id');
  if (!chat_id) {
    toast.error('Oops! Something went wrong.');
    return;
  }
  const selectedConversation = await getConversation(chat_id);
  if (!selectedConversation) {
    toast.error('Oops! Something went wrong.');
    return;
  }

  const blob = new Blob([JSON.stringify(selectedConversation, null, 2)], {
    type: 'application/json',
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.download = `conversation_${selectedConversation.name}.json`;
  link.href = url;
  link.style.display = 'none';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};