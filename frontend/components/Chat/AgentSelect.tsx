import { useContext } from 'react';

import { useTranslation } from 'next-i18next';

import { OpenAgent } from '@/types/agent';

import HomeContext from '@/pages/api/home/home.context';

import { MenuItem, Select } from '@mui/material';

export const AgentSelect = () => {
  const { t } = useTranslation('chat');

  const {
    state: { selectedConversation, agents, defaultAgentId },
    handleUpdateConversation,
  } = useContext(HomeContext);

  const handleChange = (e: any) => {
    if (!selectedConversation) return;
    const newAgent = agents.find(
      (agent) => agent.id === e.target.value,
    ) as OpenAgent;
    handleUpdateConversation(
      selectedConversation,
      {
        key: 'agent',
        value: newAgent,
      },
      false,
    );
  };

  return (
    <div className="flex flex-row">
      <div className="flex flex-col flex-1">
        <div className="w-full rounded-lg bg-transparent text-neutral-900">
          <Select
            className="rounded-xl font-[Montserrat] w-[16rem] h-8 mt-[1px] bg-transparent"
            placeholder={t('Select an agent') || ''}
            value={selectedConversation?.agent?.id || defaultAgentId}
            onChange={handleChange}
            MenuProps={{
              PaperProps: {
                className: 'rounded-xl',
                sx: {
                  '& .MuiMenuItem-root': {
                    fontFamily: 'Montserrat',
                  },
                },
              },
            }}
          >
            {agents.map((agent) => (
              <MenuItem key={agent.id} value={agent.id} className="rounded-xl">
                {agent.name}
              </MenuItem>
            ))}
          </Select>
        </div>
      </div>
    </div>
  );
};
