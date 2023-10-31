import {
  IconCheck,
  IconCopy,
  IconHeart,
  IconHeartFilled,
} from '@tabler/icons-react';
import { FC, memo, useContext, useEffect, useMemo, useState } from 'react';

import Image from 'next/image';

import useMemoDeep from '@/hooks/useMemoDeep';

import { RichContentItem } from '@/types/chat';

import HomeContext from '@/pages/api/home/home.context';

import KaggleConnector from '@/components/DataStore/KaggleConnector';
import EChartsChart from '@/components/Datatype/Chart/Echart';
import KaggleDatasetList from '@/components/Datatype/List/KaggleDatasetList';

import XLangTable from '../Datatype/Table/XLangTable';
import { CodeBlock } from '../Markdown/CodeBlock';
import { MemoizedReactMarkdown } from '../Markdown/MemoizedReactMarkdown';

import Alert from '@mui/material/Alert';
import { isEqual } from 'lodash';
import rehypeMathjax from 'rehype-mathjax';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';

interface Props {
  item: RichContentItem;
  messageIndex: number;
  itemIndex: number;
  component: string;
}

const ChatRichContentItem: FC<Props> = memo(
  ({ item, messageIndex, itemIndex, component }) => {
    const {
      state: { messageIsStreaming },
    } = useContext(HomeContext);

    useEffect(() => {
      const iframes =
        document.querySelectorAll<HTMLIFrameElement>('#my-iframe');
      iframes.forEach((iframe) => {
        iframe.onload = () => {
          const { contentWindow } = iframe;
          if (!contentWindow) return;

          const { body } = contentWindow.document;
          iframe.style.height = `${body.scrollHeight + 16}px`;
          iframe.style.width = `${body.scrollWidth + 16}px`;
        };
      });
    }, []);

    return (
      <>
        {component === 'intermediateSteps' && item.type != 'transition' ? (
          <div className="prose max-w-full">
            <ChatRichContentItemBody
              item={item}
              messageIsStreaming={messageIsStreaming}
              component={component}
              messageIndex={messageIndex}
              itemIndex={itemIndex}
            />
          </div>
        ) : (
          <div className="prose max-w-full">
            <ChatRichContentItemBody
              item={item}
              messageIsStreaming={messageIsStreaming}
              component={component}
              messageIndex={messageIndex}
              itemIndex={itemIndex}
            />
          </div>
        )}
      </>
    );
  },
  (prevProps, nextProps) => {
    return isEqual(prevProps, nextProps);
  },
);

interface ChatRichContentItemBodyProps {
  item: RichContentItem;
  messageIsStreaming: boolean;
  component: string;
  messageIndex: number;
  itemIndex: number;
}

export const ChatRichContentItemBody: FC<ChatRichContentItemBodyProps> = memo(
  ({ item, messageIsStreaming, component, messageIndex, itemIndex }) => {
    switch (item.type) {
      case 'kaggle_connect':
        return <KaggleConnector content={item.content} />;
      case 'kaggle_search':
        return <KaggleDatasetList content={item.content}></KaggleDatasetList>;
      case 'echarts':
        return <EChartsChart content={item.content}></EChartsChart>;
      case 'snowflake_connector':
        return <div></div>;
      case 'error':
        return (
          <Alert className="rounded-xl" severity="error">
            {item.content}
          </Alert>
        );
      case 'image':
        return (
          <div className="flex w-full">
            <Image
              src={item.content}
              alt="image"
              width="500"
              height="500"
              style={{ position: 'relative', height: '100%', width: '100%' }}
            />
          </div>
        );
      case 'html':
        return (
          <div className="mt-[-2px] w-full flex justify-center">
            <iframe id="my-iframe" title="my-iframe" srcDoc={item.content} />
          </div>
        );
      case 'table':
        return (
          <div className="max-w-full mt-[-5px]">
            <XLangTable content={item.content} />
          </div>
        );
      default:
        return (
          <>
            <MemoizedReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeMathjax]}
              messageIsStreaming={messageIsStreaming}
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '');
                  return !inline ? (
                    <CodeBlock
                      key={Math.random()}
                      language={(match && match[1]) || ''}
                      value={String(children).replace(/\n$/, '')}
                      component={component}
                      messageIndex={messageIndex}
                      itemIndex={itemIndex}
                      {...props}
                    />
                  ) : (
                    <code className={className} {...props}>
                      {children}
                    </code>
                  );
                },
                table({ children }) {
                  return (
                    <div className="overflow-x-auto w-full">
                      <table className="border-collapse border border-black px-3 py-1">
                        {children}
                      </table>
                    </div>
                  );
                },
                th({ children }) {
                  return (
                    <th className="break-words border border-black bg-gray-500 px-3 py-1 text-white">
                      {children}
                    </th>
                  );
                },
                td({ children }) {
                  return (
                    <td className="break-words border border-black px-3 py-1">
                      {children}
                    </td>
                  );
                },
              }}
            >
              {item.content}
            </MemoizedReactMarkdown>
          </>
        );
    }
  },
  (prevProps, nextProps) => {
    return isEqual(prevProps, nextProps);
  },
);

ChatRichContentItem.displayName = 'ChatRichContentItem';

export default ChatRichContentItem;
