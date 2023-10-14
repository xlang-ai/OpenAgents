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
import Link from '@mui/material/Link';

export type PluginChangeHandler = (plugin: Plugin, selected: boolean) => void;

export const PluginSelect = () => {
  const {
    state: { pluginsIsSelected, pluginList, selectedConversation },
    dispatch: homeDispatch,
  } = useContext(HomeContext);

  const togglePluginSelection = (plugin: Plugin) => {
    const pluginID = plugin.id;
    if (plugin.require_api_key && plugin.api_key == null) {
    } else {
      let updatedPluginsIsSelected: Record<string, boolean | undefined> = {};
      if (pluginID == 'AUTO' && !pluginsIsSelected[pluginID]) {
        updatedPluginsIsSelected = { AUTO: true };
      } else {
        updatedPluginsIsSelected = {
          ...pluginsIsSelected,
          [pluginID]: !pluginsIsSelected[pluginID],
        };
      }
      homeDispatch({
        field: 'pluginsIsSelected',
        value: updatedPluginsIsSelected,
      });
      console.log(pluginsIsSelected);
      console.log(pluginID);
      return;
    }
  };

  useEffect(() => {
    let updatedSelectedPlugins = pluginList.filter(
      (plugin) => pluginsIsSelected[plugin.id],
    );
    if (pluginsIsSelected['AUTO']) {
      updatedSelectedPlugins = pluginList.filter(
        (plugin) => plugin.id == 'AUTO',
      );
    }
    homeDispatch({ field: 'selectedPlugins', value: updatedSelectedPlugins });
    const updatedConversation = {
      ...selectedConversation,
      selectedPlugins: updatedSelectedPlugins,
    };
    homeDispatch({ field: 'selectedConversation', value: updatedConversation });
  }, [pluginsIsSelected, pluginList]);

  return (
    <div className="flex flex-col w-full">
      <SelectedPlugin />
      <PluginList
        plugins={pluginList}
        pluginsIsSelected={pluginsIsSelected}
        togglePluginSelection={togglePluginSelection}
      />
    </div>
  );
};

export const SelectedPlugin = ({
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
            selectedConversation.selectedPlugins.length > 0 && (
              <div className="flex gap-1 w-full h-full items-center pl-3">
                {selectedConversation.selectedPlugins.map((plugin) => (
                  <div
                    className={`overflow-hidden relative ${
                      compact ? 'w-full h-full' : 'w-6 h-6'
                    } flex items-center justify-center`}
                    key={plugin.id}
                  >
                    {plugin.icon ? (
                      <img
                        className={`text-[#343541] ${
                          compact ? '!h-4 !w-4' : 'w-full h-full'
                        }`}
                        src={plugin.icon}
                        alt={plugin.nameForHuman}
                      />
                    ) : (
                      <ExtensionOutlinedIcon
                        className={`text-[#343541] ${
                          compact ? '!h-4 !w-4' : 'w-full h-full'
                        }`}
                      />
                    )}
                  </div>
                ))}
              </div>
            )}
          {selectedConversation?.selectedPlugins.length === 0 && (
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
    state: { pluginListLoading, selectedConversation },
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
          homeDispatch({ field: 'apiKeyUploading', value: false });
        } else {
          homeDispatch({ field: 'apiKeyUploading', value: false });
          if (hoveredPlugin) {
            hoveredPlugin.api_key = apiKey;
          }
        }
      } catch (error) {
        homeDispatch({ field: 'apiKeyUploading', value: false });
        toast.error((error as Error).message);
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

  return (
    <div className="relative mt-3 w-[16rem]">
      <div className="rounded-xl bg-white border border-[#c4c4c4] flex max-h-[11rem] w-full max-w-xs flex-col overflow-hidden text-base focus:outline-none sm:text-sm md:w-[100%]">
        {pluginListLoading ? (
          <div className="flex justify-center items-center h-32">
            <div className="h-4 w-4 animate-spin rounded-full border-t-2 border-neutral-800 opacity-60"></div>
          </div>
        ) : (
          <ul className="overflow-auto">
            {plugins.map((plugin) => {
              let disable: boolean;
              disable =
                ((plugin.name != 'auto' && pluginsIsSelected['AUTO']) ||
                  (selectedConversation?.selectedPlugins.length == 5 &&
                    !selectedConversation?.selectedPlugins.includes(plugin))) ??
                false;
              return (
                <li
                  key={plugin.id}
                  className={`group relative flex h-[50px] select-none items-center overflow-hidden border-b border-black/10 pl-5 pr-12 last:border-0 text-[#202123] hover:bg-[#ececf1]/70 transition-colors ${
                    disable ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
                  } `}
                  onClick={() => {
                    if (disable) {
                      if (pluginsIsSelected['AUTO']) {
                        toast.error(
                          "You can't select auto and other plugins at the same time.",
                        );
                      } else {
                        toast.error("You can't select more than 5 plugins.");
                      }
                    } else {
                      togglePluginSelection(plugin);
                    }
                  }}
                  onMouseEnter={(e) => handleMouseEnter(plugin)}
                >
                  <span className="flex items-center gap-2 truncate">
                    <span className="h-6 w-6 shrink-0">
                      {plugin.icon.startsWith('data:image') ? (
                        <img src={plugin.icon} alt={plugin.nameForHuman} />
                      ) : (
                        <ExtensionOutlinedIcon className="text-[#343541]" />
                      )}
                    </span>
                    <span className="flex items-center gap-1 text-[#343541]">
                      {plugin.nameForHuman}
                    </span>
                  </span>
                  <span className="absolute inset-y-0 right-0 flex items-center pr-5 text-[#343541]">
                    {pluginsIsSelected[plugin.id] ? (
                      <CheckBoxIcon />
                    ) : (
                      <CheckBoxOutlineBlankIcon
                        className={disable ? `text-gray-400` : ''}
                      />
                    )}
                  </span>
                </li>
              );
            })}
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
                <div>
                  <div
                    className="font-bold text-[#ff0000] text-sm"
                    style={{ marginTop: 10, marginBottom: 10 }}
                  >
                    *This plugin requires API key
                  </div>
                  <div
                    style={{
                      marginTop: 10,
                      marginBottom: 10,
                      marginLeft: 5,
                      cursor: 'grab',
                    }}
                  >
                    <Link
                      className="text-sm"
                      onClick={() => {
                        window.open(
                          'https://docs.xlang.ai/user-manual/plugins-agent-auth',
                        );
                      }}
                    >
                      Click here for instructions to get API key
                    </Link>
                  </div>
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
            <div className="flex font-bold text-[#343541]">
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
