import { KeyValuePair } from './data';

export interface Plugin {
  id: string;
  name: string;
  nameForHuman: string;
  prettyNameForHuman?: string;
  type?: string;
  icon: string;
  iconId?: string;
  description: string;
  require_api_key: boolean;
  api_key: string;
  requiredKeys?: KeyValuePair[];
}

export interface PluginKey {
  pluginId: PluginID;
  requiredKeys: KeyValuePair[];
}

export enum PluginID {
  GOOGLE_SEARCH = 'google-search',
}

export enum PluginName {
  GOOGLE_SEARCH = 'Google Search',
}
