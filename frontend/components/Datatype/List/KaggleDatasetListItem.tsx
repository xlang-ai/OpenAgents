import React, { FC, memo, useContext } from 'react';
import toast from 'react-hot-toast';

import { API_KAGGLE_DOWNLOAD_DATASET } from '@/utils/app/const';

import { KaggleSearchItem } from '@/types/kaggle';

import HomeContext from '@/pages/api/home/home.context';

import { LikeOutlined, StarOutlined } from '@ant-design/icons';

interface Props {
  item: KaggleSearchItem;
}

const KaggleDatasetListItem: FC<Props> = memo(({ item }) => {
  const {
    state: { chat_id },
    handleFetchDataPath,
    dispatch: homeDispatch,
  } = useContext(HomeContext);

  const handleDownload = () => {
    homeDispatch({
      field: 'messageIsStreaming',
      value: true,
    });
    fetch(API_KAGGLE_DOWNLOAD_DATASET, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chat_id: chat_id,
        url: item.id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data || !data.success) {
          toast.error(data.message);
          homeDispatch({
            field: 'messageIsStreaming',
            value: false,
          });
          return;
        }
        handleFetchDataPath(chat_id, data.data_path);
        homeDispatch({
          field: 'messageIsStreaming',
          value: false,
        });
      })
      .catch((error) => {
        toast.error(error.message);
        homeDispatch({
          field: 'messageIsStreaming',
          value: false,
        });
      });
  };

  return (
    <div className="relative flex flex-col rounded-xl border border-[#D8D8D8] p-3 space-y-2 w-full h-32 mb-4">
      <div className="font-[600] text-base max-w-[75%] overflow-auto">
        {item.title}
      </div>
      <div className="font-[400] mr-20 text-sm max-w-[75%] overflow-auto">
        {item.description}
      </div>
      <div className="absolute bottom-3 font-[500] text-[#7B7B7B] text-sm">
        <StarOutlined size={24} rev={undefined} />
        <span className="absolute left-[1.5rem] -bottom-[2.5px]">
          {item.downloads}
        </span>
        <LikeOutlined
          size={24}
          rev={undefined}
          className="absolute left-[6rem] bottom-[2px]"
        />
        <span className="absolute left-[7.6rem] -bottom-[2.5px]">
          {item.likes}
        </span>
        <button
          onClick={handleDownload}
          className="text-[#0156AC] border border-[#0156AC] rounded-lg px-2 py-1 text-xs absolute left-[11.1rem] -bottom-1"
        >
          Download
        </button>
      </div>
      <img
        alt="logo"
        className="absolute right-3 w-[20%] h-[50%] top-[50%] translate-y-[-60%]"
        src={item.image}
      ></img>
    </div>
  );
});

export default KaggleDatasetListItem;
