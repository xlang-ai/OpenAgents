import {
  Conversation,
  ConversationNameListItem,
  RichContentItem,
} from '@/types/chat';

import {
  API_CLEAR_CONVERSATIONS,
  API_CONVERSATION_LIST,
  API_DELETE_CONVERSATION,
  API_GET_CONVERSATION,
  API_IMPORT_CONVERSATIONS,
  API_REGISTER_CONVERSATION,
  API_UPDATE_CONVERSATION,
  API_STOP_CONVERSATION,
} from './const';
import toast from 'react-hot-toast';


export const updateConversation = (
  updatedConversation: Conversation,
  allConversations: Conversation[],
) => {
  const updatedConversations = allConversations.map((c) => {
    if (c.id === updatedConversation.id) {
      return updatedConversation;
    }

    return c;
  });

  saveConversation(updatedConversation);
  saveConversations(updatedConversations);

  return {
    single: updatedConversation,
    all: updatedConversations,
  };
};

export const saveConversation = (conversation?: Conversation) => {
  if (conversation) {
    localStorage.setItem('selectedConversation', JSON.stringify(conversation));
  } else {
    localStorage.removeItem('selectedConversation');
  }
};

export const saveConversations = (conversations: Conversation[]) => {
  localStorage.setItem('conversationHistory', JSON.stringify(conversations));
};

export const findRichContentByID = (
  conversation: Conversation,
  id: number,
): RichContentItem | null => {
  for (const message of conversation.messages) {
    const { intermediateSteps, finalAnswer } = message.richContent ?? {};

    if (intermediateSteps) {
      for (const step of intermediateSteps) {
        if (id === step.id) return step;
      }
    }

    if (finalAnswer) {
      for (const step of finalAnswer) {
        if (id === step.id) return step;
      }
    }
  }

  return null;
};

export const registerConversation = async (conversation: Conversation) => {
  let response;
  try {
    response = await fetch(API_REGISTER_CONVERSATION, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          conversation: conversation,
        }),
      });
  } catch (error: unknown) {
    toast.error('Error registering conversation!');
    throw error;
  }
  
  if (!response.ok) {
    toast.error(response.statusText);
    return {
      id: null,
    };
  }
  const data = await response.json();
  if (!data) {
    toast.error('Error registering conversation!');
    return {
      id: null,
    };
  }
  return data;
};

export const stopConversation = async (chat_id: string) => {
  let response;
  try {
    response = await fetch(API_STOP_CONVERSATION, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        chat_id: chat_id,
      }),
    });
  } catch (error: unknown) {
    toast.error('Error stopping conversation!');
    throw error;
  }
  
  if (!response.ok) {
    toast.error(response.statusText);
    return;
  }
  const data = await response.json();
  if (!data || !data["success"]) {
    toast.error("Error stopping conversation!");
  }
  return;
};

export const updateConversationNameList = async (conversationsToUpdate: Conversation[] | ConversationNameListItem[]) => {
  let response;
  try {
    response = await fetch(API_UPDATE_CONVERSATION, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        conversations: conversationsToUpdate,
      }),
    });
  } catch (error: unknown) {
    toast.error('Error updating conversations!');
    throw error;
  }
    
  if (!response.ok) {
    toast.error(response.statusText);
    return;
  }
  const data = await response.json();
  if (!data || !data["success"]) {
    toast.error(data["message"]);
  }
}


export const getConversationNameList = async (page: number = 1) => {
  let response;
  try {
    response = await fetch(API_CONVERSATION_LIST, {
      method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          page: page
        }),
    });
  } catch (error: unknown) {
    toast.error('Error getting conversation list!');
    throw error;
  }
  
  if (!response.ok) {
    toast.error(response.statusText);
    return [];
  }
  const data: ConversationNameListItem[] = await response.json();
  return data;
};

export const clearAllConversations = async () => {
  let response;
  try {
    response = await fetch(API_CLEAR_CONVERSATIONS, {
      method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
    });
  } catch (error: unknown) {
    toast.error('Error clearing all conversations!');
    throw error;
  }
  
  if (!response.ok) {
    toast.error(response.statusText);
    return;
  }
  const data = await response.json();
  if (!data || !data["success"]) {
    toast.error("Error clearing all conversations!");
    return;
  }
};

// unused
export const importConversations = async (conversations: Conversation[]) => {
  const response = await fetch(API_IMPORT_CONVERSATIONS, {
    method: 'PATCH',
    body: JSON.stringify(conversations),
  });
  return response;
};

export const deleteConversation = async (
  conversation: Conversation | ConversationNameListItem,
) => {
  let response;
  try {
    response = await fetch(API_DELETE_CONVERSATION, {
      method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          chat_id: conversation.id
        }),
    });
  } catch (error: unknown) {
    toast.error('Error deleting conversation!');
    throw error;
  }
  
  if (!response.ok) {
    toast.error(response.statusText);
    return;
  }
  const data = await response.json();
  if (!data || !data["success"]) {
    toast.error("Error deleting conversation!");
    return;
  }
}


export const getConversation = async (
  conversation_id: string | null,
) => {
  let response;
  try {
    response = await fetch(API_GET_CONVERSATION, {
      method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        body: JSON.stringify({
          chat_id: conversation_id
        }),
    });
  } catch (error: unknown) {
    toast.error('Error getting conversation!');
    throw error;
  }
  
  if (!response.ok) {
    toast.error(response.statusText);
    return undefined
  }
  const conversation: Conversation = await response.json();
  if (!conversation.selectedCodeInterpreterPlugins)
    conversation.selectedCodeInterpreterPlugins= []
  if (!conversation.selectedPlugins)
    conversation.selectedPlugins = []
  return conversation;
};