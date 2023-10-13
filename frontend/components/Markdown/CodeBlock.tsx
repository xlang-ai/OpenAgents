import { IconCheck, IconClipboard, IconDownload } from '@tabler/icons-react';
import React, { FC, memo, useState } from 'react';
import toast from 'react-hot-toast';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/cjs/styles/prism';

import { useTranslation } from 'next-i18next';

import {
  generateRandomString,
  programmingLanguages,
} from '@/utils/app/codeblock';

import CodeModal from '../CodeModal/CodeModal';

interface Props {
  language: string;
  value: string;
  component: string;
  messageIndex: number;
  itemIndex: number;
}

export const CodeBlock: FC<Props> = memo(
  ({ language, value, component, messageIndex, itemIndex }) => {
    const { t } = useTranslation('markdown');

    const [isCopied, setIsCopied] = useState<Boolean>(false);
    const [code, setCode] = useState(value);
    const [openModal, setOpenModal] = useState<boolean>(false);

    const copyToClipboard = () => {
      if (!navigator.clipboard || !navigator.clipboard.writeText) {
        return;
      }

      navigator.clipboard.writeText(value).then(() => {
        setIsCopied(true);
        toast.success('Copied!');

        setTimeout(() => {
          setIsCopied(false);
        }, 2000);
      });
    };
    const downloadAsFile = () => {
      const fileExtension = programmingLanguages[language] || '.file';
      const suggestedFileName = `file-${generateRandomString(
        3,
        true,
      )}${fileExtension}`;
      const fileName = window.prompt(
        t('Enter file name') || '',
        suggestedFileName,
      );

      if (!fileName) {
        // user pressed cancel on prompt
        return;
      }

      const blob = new Blob([value], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.download = fileName;
      link.href = url;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    };

    return (
      <div className="codeblock relative font-consolas text-[16px]">
        <div className="flex items-center justify-between py-1 px-4 bg-[#212121]">
          <span className="text-sm lowercase text-white">{language}</span>

          <div className="flex items-center">
            <button
              className="flex gap-1.5 items-center rounded bg-none p-1 text-xs text-white"
              onClick={copyToClipboard}
            >
              {isCopied ? (
                <IconCheck color="white" size={20} />
              ) : (
                <IconClipboard color="white" size={20} />
              )}
            </button>
            <button
              className="flex items-center rounded bg-none p-1 text-xs text-white"
              onClick={downloadAsFile}
            >
              <IconDownload color="white" size={20} />
            </button>
          </div>
        </div>

        <SyntaxHighlighter
          language={language}
          style={oneLight}
          wrapLines={true}
          wrapLongLines={true}
          customStyle={{
            margin: 0,
            border: '1px solid #212121',
            borderRadius: '0 0 5px 5px',
          }}
        >
          {code}
        </SyntaxHighlighter>

        {openModal && (
          <CodeModal
            setOpenModal={setOpenModal}
            setCode={setCode}
            code={code}
            component={component}
            messageIndex={messageIndex}
            itemIndex={itemIndex}
            language={language}
          />
        )}
      </div>
    );
  },
);
CodeBlock.displayName = 'CodeBlock';
