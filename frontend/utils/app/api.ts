import { Plugin, PluginID } from '@/types/plugin';

import { API_CHAT, API_RECOMMEND, API_CHAT_XLANG, API_CHAT_XLANG_PLUGIN , API_CHAT_XLANG_WEBOT} from './const';
import { OpenAIModel, OpenAIModelID } from '@/types/openai';

export const getEndpoint = (model: OpenAIModel) => {
  if (model.id === OpenAIModelID.XLANG_DATACOPILOT) {
    return API_CHAT;
  }
  // if (model.id === OpenAIModelID.XLANG_CHAT) {
  //   return API_CHAT_XLANG;
  // }
  if (model.id === OpenAIModelID.XLANG_PLUGIN) {
    return API_CHAT_XLANG_PLUGIN;
  }
  if (model.id === OpenAIModelID.XLANG_WEBOT) {
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
