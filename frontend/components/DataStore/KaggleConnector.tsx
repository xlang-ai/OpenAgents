import React, { FC, memo, useContext, useState } from 'react';
import toast from 'react-hot-toast';

import { API_KAGGLE_DOWNLOAD_DATASET } from '@/utils/app/const';

import HomeContext from '@/pages/api/home/home.context';

import { Button, Form, Input } from 'antd';

interface Props {
  content: string;
}

const KaggleConnector: FC<Props> = memo(({ content }) => {
  const {
    state: { chat_id },
    handleFetchDataPath,
    dispatch: homeDispatch,
  } = useContext(HomeContext);

  const [form] = Form.useForm();
  const [downloading, setDownloading] = useState(false);

  const onFinish = (values: any) => {
    values.chat_id = chat_id;
    homeDispatch({
      field: 'messageIsStreaming',
      value: true,
    });
    setDownloading(true);
    fetch(API_KAGGLE_DOWNLOAD_DATASET, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(values),
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data || !data.success) {
          toast.error(data.message);
          homeDispatch({
            field: 'messageIsStreaming',
            value: false,
          });
        }
        handleFetchDataPath(chat_id, data.data_path);
        homeDispatch({
          field: 'messageIsStreaming',
          value: false,
        });
        setDownloading(false);
      })
      .catch((error) => {
        toast.error(error.message);
        homeDispatch({
          field: 'messageIsStreaming',
          value: false,
        });
        setDownloading(false);
      });
  };

  return (
    <div>
      Please enter the url of the dataset you want to connect to.
      <Form
        form={form}
        style={{ marginTop: 25 }}
        initialValues={{
          remember: true,
          url: content
            ? `www.kaggle.com/datasets/${content}`
            : `www.kaggle.com/datasets/`,
        }}
        onFinish={onFinish}
      >
        <Form.Item
          name="url"
          rules={[
            { required: true, message: 'Please enter Kaggle dataset URL.' },
          ]}
        >
          <Input addonBefore="https://" />
        </Form.Item>
        <Form.Item>
          <div style={{ textAlign: 'right' }}>
            <Button loading={downloading} htmlType="submit">
              Download Dataset
            </Button>
          </div>
        </Form.Item>
      </Form>
    </div>
  );
});

export default KaggleConnector;
