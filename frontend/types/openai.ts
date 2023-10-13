import { OPENAI_API_TYPE } from '../utils/app/const';

export interface OpenAIModel {
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

export enum OpenAIModelID {
  XLANG_DATACOPILOT = 'xlang-datacopilot',
  XLANG_PLUGIN = 'xlang-plugins',
  XLANG_WEBOT = 'xlang-webot',
}

// in case the `DEFAULT_MODEL` environment variable is not set or set to an unsupported model
export const fallbackModelID = OpenAIModelID.XLANG_DATACOPILOT;

export const OpenAIModels: Record<OpenAIModelID, OpenAIModel> = {
  [OpenAIModelID.XLANG_DATACOPILOT]: {
    id: OpenAIModelID.XLANG_DATACOPILOT,
    name: 'Data Agent',
    maxLength: 12000,
    tokenLimit: 4000,
    llm: undefined,
  },
  [OpenAIModelID.XLANG_PLUGIN]: {
    id: OpenAIModelID.XLANG_PLUGIN,
    name: 'Plugins Agent',
    maxLength: 1024,
    tokenLimit: 4000,
    llm: undefined,
  },
  [OpenAIModelID.XLANG_WEBOT]: {
    id: OpenAIModelID.XLANG_WEBOT,
    name: 'Web Agent',
    maxLength: 1024,
    tokenLimit: 4000,
    llm: undefined,
  },
};

export const OpenAIModelList = Object.values(OpenAIModels);
