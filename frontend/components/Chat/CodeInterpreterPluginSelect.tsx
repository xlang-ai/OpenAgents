import { useCallback, useContext, useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';

import { useTranslation } from 'next-i18next';

import { API_POST_API_KEY } from '@/utils/app/const';

import { Plugin } from '@/types/plugin';

import HomeContext from '@/pages/api/home/home.context';

import { ApiKeyInput } from './ApiKeyInput';

import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import ComputerOutlinedIcon from '@mui/icons-material/ComputerOutlined';
import ExtensionOutlinedIcon from '@mui/icons-material/ExtensionOutlined';

export type PluginChangeHandler = (plugin: Plugin, selected: boolean) => void;

export const CodeInterpreterPluginSelect = () => {
  const {
    state: {
      codeInterpreterPluginsIsSelected,
      codeInterpreterPluginList,
      selectedConversation,
    },
    dispatch: homeDispatch,
  } = useContext(HomeContext);

  const togglePluginSelection = (plugin: Plugin) => {
    const pluginID = plugin.id;
    if (plugin.require_api_key && plugin.api_key == null) {
    } else {
      const updatedPluginsIsSelected = {
        ...codeInterpreterPluginsIsSelected,
        [pluginID]: !codeInterpreterPluginsIsSelected[pluginID],
      };
      homeDispatch({
        field: 'codeInterpreterPluginsIsSelected',
        value: updatedPluginsIsSelected,
      });
    }
  };

  useEffect(() => {
    const updatedSelectedPlugins = codeInterpreterPluginList.filter(
      (plugin) => codeInterpreterPluginsIsSelected[plugin.id],
    );
    homeDispatch({
      field: 'selectedCodeInterpreterPlugins',
      value: updatedSelectedPlugins,
    });
    const updatedConversation = {
      ...selectedConversation,
      selectedCodeInterpreterPlugins: updatedSelectedPlugins,
    };
    homeDispatch({ field: 'selectedConversation', value: updatedConversation });
  }, [codeInterpreterPluginsIsSelected, codeInterpreterPluginList]);

  return (
    <div className="flex flex-col">
      <SelectedCodeInterpreterPlugin />
      <PluginList
        plugins={codeInterpreterPluginList}
        pluginsIsSelected={codeInterpreterPluginsIsSelected}
        togglePluginSelection={togglePluginSelection}
      />
    </div>
  );
};

export const SelectedCodeInterpreterPlugin = ({
  onClick,
  compact,
}: {
  onClick?: () => void;
  compact?: boolean;
}) => {
  const {
    state: { selectedConversation },
  } = useContext(HomeContext);

  const { t } = useTranslation('chat');

  return (
    <div className="relative flex rounded-xl w-[16rem] h-8 bg-transparent border border-[#c4c4c4] overflow-hidden">
      <button onClick={onClick}>
        <span className="flex w-[12.5rem] leading-8 h-8 pr-6 overflow-hidden">
          {selectedConversation &&
            selectedConversation.selectedCodeInterpreterPlugins.length > 0 && (
              <div className="flex gap-1 w-full h-full items-center pl-3">
                {selectedConversation.selectedCodeInterpreterPlugins.map(
                  (plugin) => (
                    <div
                      className={`overflow-hidden relative ${
                        compact ? 'w-full h-full' : 'w-6 h-6'
                      } flex items-center justify-center`}
                      key={plugin.id}
                    >
                      {plugin.icon ? (
                        <img
                          className={`text-[#343541]  ${
                            compact ? '!h-4 !w-4' : 'w-full h-full'
                          }`}
                          src={plugin.icon}
                          alt={plugin.name}
                        />
                      ) : (
                        <ExtensionOutlinedIcon
                          className={`text-[#343541] ${
                            compact ? '!h-4 !w-4' : 'w-full h-full'
                          }`}
                        />
                      )}
                    </div>
                  ),
                )}
              </div>
            )}
          {selectedConversation &&
            selectedConversation.selectedCodeInterpreterPlugins.length ===
              0 && (
              <span
                className={`flex items-center text-[15px] text-[#212121] pl-3`}
              >
                {t('No plugins enabled')}
              </span>
            )}
        </span>
        <ArrowDropUpIcon className="w-[2rem] text-[#757575] absolute top-1 right-[2px] cursor-default" />
      </button>
    </div>
  );
};

const PluginList = ({
  plugins,
  pluginsIsSelected,
  togglePluginSelection,
}: {
  plugins: Plugin[];
  pluginsIsSelected: Partial<Record<string, boolean>>;
  togglePluginSelection: (plugin: Plugin) => void;
}) => {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const divRef = useRef<HTMLDivElement>(null);

  const {
    state: { codeInterpreterPluginListLoading },
    dispatch: homeDispatch,
  } = useContext(HomeContext);

  const [hoveredPlugin, setHoveredPlugin] = useState<Plugin | null>(null);

  const handleMouseEnter = (plugin: Plugin) => {
    setHoveredPlugin(plugin);
  };

  const handleConfirm = useCallback(
    async (apiKey: string) => {
      homeDispatch({ field: 'apiKeyUploading', value: true });
      const endpoint = API_POST_API_KEY;
      const body = JSON.stringify({
        tool_id: hoveredPlugin?.id,
        tool_name: hoveredPlugin?.name,
        api_key: apiKey,
      });
      let response;
      try {
        response = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
          body,
        });
        if (!response.ok) {
          toast.error('Error uploading API key!');
        }
        homeDispatch({ field: 'apiKeyUploading', value: false });
      } catch (error) {
        homeDispatch({ field: 'apiKeyUploading', value: false });
        toast.error('Error uploading API key!');
      }
    },
    [hoveredPlugin],
  );
  useEffect(() => {
    if (hoveredPlugin?.require_api_key && hoveredPlugin.api_key == null) {
      const element = divRef.current;
      if (element) element.scrollTop = element.scrollHeight;
    }
  }, [hoveredPlugin]);
  useEffect(() => {}, [handleConfirm]);

  const languagePlugins = plugins.filter(
    (plugin) => plugin.type === 'language',
  );
  const toolPlugins = plugins.filter((plugin) => plugin.type === 'tool');

  return (
    <div className="relative mt-3 w-[16rem]">
      <div className="rounded-xl bg-white border border-[#c4c4c4] flex max-h-[11rem] w-full max-w-xs flex-col overflow-hidden text-base focus:outline-none sm:text-sm md:w-[100%]">
        {codeInterpreterPluginListLoading ? (
          <div className="flex justify-center items-center h-32">
            <div className="h-4 w-4 animate-spin rounded-full border-t-2 border-neutral-800 opacity-60"></div>
          </div>
        ) : (
          <ul className="overflow-auto">
            <li
              className="group relative flex h-[50px] cursor-pointer select-none items-center overflow-hidden border-b border-black/10 pl-5 last:border-0 hover:bg-[#ececf1]/70 transition-colors"
              key="language-plugins"
            >
              Programming Languages
            </li>
            {languagePlugins.map((plugin) => (
              <li
                className="group relative flex h-[50px] cursor-pointer select-none items-center overflow-hidden border-b border-black/10 pl-5 last:border-0 text-[#202123] hover:bg-[#ececf1]/70 transition-colors"
                key={plugin.id}
                onClick={() => {
                  togglePluginSelection(plugin);
                }}
                onMouseEnter={() => handleMouseEnter(plugin)}
              >
                <span className="flex items-center gap-2 truncate ml-1">
                  <span className="h-6 w-6 shrink-0">
                    <img src={plugin.icon} alt={plugin.nameForHuman} />
                  </span>
                  <span className="flex items-center gap-1 text-[#343541]">
                    {plugin.nameForHuman}
                  </span>
                </span>
                <span className="absolute inset-y-0 right-0 flex items-center pr-5 text-[#343541]">
                  {pluginsIsSelected[plugin.id] ? (
                    <CheckBoxIcon />
                  ) : (
                    <CheckBoxOutlineBlankIcon />
                  )}
                </span>
              </li>
            ))}
            <li
              className="group relative flex h-[50px] cursor-pointer select-none items-center overflow-hidden border-b border-black/10 pl-5 pr-12 last:border-0 text-[#202123] hover:bg-[#ececf1]/70 transition-colors"
              key="language-plugins"
            >
              Data Tools
            </li>
            {toolPlugins.map((plugin) => (
              <li
                className="group relative flex h-[50px] cursor-pointer select-none items-center overflow-hidden border-b border-black/10 pl-5 pr-12 last:border-0 text-[#202123] hover:bg-[#ececf1]/70 transition-colors"
                key={plugin.id}
                onClick={() => {
                  togglePluginSelection(plugin);
                }}
                onMouseEnter={() => handleMouseEnter(plugin)}
              >
                <span className="flex items-center gap-2 truncate ml-1">
                  <span className="h-6 w-6 shrink-0">
                    <img src={plugin.icon} alt={plugin.nameForHuman} />
                  </span>
                  <span className="flex h-6 items-center gap-1 text-[#343541]">
                    {plugin.nameForHuman}
                  </span>
                </span>
                <span className="absolute inset-y-0 right-0 flex items-center pr-5 text-[#343541]">
                  {pluginsIsSelected[plugin.id] ? (
                    <CheckBoxIcon />
                  ) : (
                    <CheckBoxOutlineBlankIcon />
                  )}
                </span>
              </li>
            ))}
            <PluginStore />
          </ul>
        )}
      </div>

      <div className="absolute top-[-2.8rem] w-[16rem] left-[19rem] z-[999] rounded-xl bg-white border border-[#c4c4c4] w-60 bg-white rounded-lg p-2 flex flex-col gap-2 h-[13.75rem]">
        {hoveredPlugin ? (
          <>
            <div className="flex space-x-2 items-center">
              <div className="border border-black/10 w-fit h-fit p-1 rounded-lg">
                {hoveredPlugin.icon ? (
                  <img
                    className="h-6 w-6 shrink-0"
                    src={hoveredPlugin.icon}
                    alt={hoveredPlugin.nameForHuman}
                  />
                ) : (
                  <ExtensionOutlinedIcon className="text-[#343541]" />
                )}
              </div>
              <div className="font-bold text-[#343541]">
                {hoveredPlugin.nameForHuman}
              </div>
            </div>
            <div
              ref={divRef}
              className="flex-1 overflow-auto text-[#343541] text-base"
            >
              {hoveredPlugin.description ?? 'No description'}
              {hoveredPlugin.require_api_key &&
              hoveredPlugin.api_key == null ? (
                <div
                  className="font-bold text-[#ff0000]]"
                  style={{ marginTop: 10, marginBottom: 10 }}
                >
                  *This plugin requires API key
                </div>
              ) : (
                <></>
              )}
              {hoveredPlugin.require_api_key &&
              hoveredPlugin.api_key != null ? (
                <div
                  className="font-bold text-[#343541]"
                  style={{ marginTop: 10, marginBottom: 10 }}
                >
                  Your api key here:{' '}
                </div>
              ) : (
                <></>
              )}
              {hoveredPlugin.require_api_key ? (
                <ApiKeyInput
                  currentPlugin={hoveredPlugin}
                  textareaRef={textareaRef}
                  onConfirm={(apiKey) => {
                    handleConfirm(apiKey);
                  }}
                />
              ) : (
                <></>
              )}
            </div>
          </>
        ) : (
          <>
            <div className="flex font-bold text-[#343541]]">
              Plugin Description
            </div>
            <div className="flex-1 overflow-auto text-[#343541] text-base">
              Select a plugin to view its description
            </div>
          </>
        )}
      </div>
    </div>
  );
};

const PluginStore = () => {
  return (
    <li className="group relative flex h-[50px] cursor-pointer select-none items-center overflow-hidden border-b border-black/10 pl-5 pr-12 last:border-0 text-[#202123] hover:bg-[#ececf1]/70 transition-colors">
      <div className="text-[#ececf1]">Plugin Store (coming soon...)</div>
      <span className="absolute inset-y-0 right-0 flex items-center pr-5 text-[#ececf1]">
        <ArrowForwardIcon />
      </span>
    </li>
  );
};
