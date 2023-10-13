import { FC, memo } from 'react';
import ReactMarkdown, { Options } from 'react-markdown';

import isEqual from 'lodash/isEqual';

interface CustomOptions {
  messageIsStreaming: boolean;
}

export const MemoizedReactMarkdown: FC<Options & CustomOptions> = memo(
  ({ messageIsStreaming, ...props }) => <ReactMarkdown {...props} />,
  (prevProps, nextProps) => isEqual(prevProps, nextProps),
);
