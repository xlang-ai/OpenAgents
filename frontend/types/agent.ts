import { OPENAI_API_TYPE } from '../utils/app/const';

export interface OpenAgent {
  id: string;
  name: string;
  maxLength: number; // maximum length of a message
  tokenLimit: number;
  llm: LLM | undefined;
}

export interface LLM {
  id: string;
  name: string;
  // TODO: other args
}

export enum OpenAgentID {
  DATA_AGENT = 'data-agent',
  PLUGINS_AGENT = 'plugins-agent',
  WEB_AGENT = 'web-agent',
}

// in case the `DEFAULT_MODEL` environment variable is not set or set to an unsupported model
export const fallbackModelID = OpenAgentID.DATA_AGENT;

export const OpenAgents: Record<OpenAgentID, OpenAgent> = {
  [OpenAgentID.DATA_AGENT]: {
    id: OpenAgentID.DATA_AGENT,
    name: 'Data Agent',
    maxLength: 12000,
    tokenLimit: 4000,
    llm: undefined,
  },
  [OpenAgentID.PLUGINS_AGENT]: {
    id: OpenAgentID.PLUGINS_AGENT,
    name: 'Plugins Agent',
    maxLength: 1024,
    tokenLimit: 4000,
    llm: undefined,
  },
  [OpenAgentID.WEB_AGENT]: {
    id: OpenAgentID.WEB_AGENT,
    name: 'Web Agent',
    maxLength: 1024,
    tokenLimit: 4000,
    llm: undefined,
  },
};

export const OpenAgentList = Object.values(OpenAgents);
