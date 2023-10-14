import { useContext } from 'react';

import { useTranslation } from 'next-i18next';

import { OpenAIModel } from '@/types/openai';

import HomeContext from '@/pages/api/home/home.context';

import { MenuItem, Select } from '@mui/material';

export const ModelSelect = () => {
  const { t } = useTranslation('chat');

  const {
    state: { selectedConversation, models, defaultModelId },
    handleUpdateConversation,
  } = useContext(HomeContext);

  const handleChange = (e: any) => {
    if (!selectedConversation) return;
    const newModel = models.find(
      (model) => model.id === e.target.value,
    ) as OpenAIModel;
    handleUpdateConversation(
      selectedConversation,
      {
        key: 'model',
        value: newModel,
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
            placeholder={t('Select a model') || ''}
            value={selectedConversation?.model?.id || defaultModelId}
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
            {models.map((model) => (
              <MenuItem key={model.id} value={model.id} className="rounded-xl">
                {model.name}
              </MenuItem>
            ))}
          </Select>
        </div>
      </div>
    </div>
  );
};
