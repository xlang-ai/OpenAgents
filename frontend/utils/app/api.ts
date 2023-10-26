import { Plugin, PluginID } from '@/types/plugin';

import { API_CHAT, API_RECOMMEND, API_CHAT_XLANG, API_CHAT_XLANG_PLUGIN , API_CHAT_XLANG_WEBOT} from './const';
import { OpenAgent, OpenAgentID } from '@/types/agent';

export const getEndpoint = (agent: OpenAgent) => {
  if (agent.id === OpenAgentID.DATA_AGENT) {
    return API_CHAT;
  }
  if (agent.id === OpenAgentID.PLUGINS_AGENT) {
    return API_CHAT_XLANG_PLUGIN;
  }
  if (agent.id === OpenAgentID.WEB_AGENT) {
    return API_CHAT_XLANG_WEBOT;
  }
  return ''
};

export const getRecommendationEndpoint = () => {
  return API_RECOMMEND;
};


const exportObjects = {
  getEndpoint,
  getRecommendationEndpoint,
};

export default exportObjects;
