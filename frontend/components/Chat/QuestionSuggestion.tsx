import { FC, useEffect, useRef } from 'react';

import { Message } from '@/types/chat';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';

interface Props {
  followUpQuestions: string[];
  onClick: (message: Message) => void;
  scrollToBottom: () => void;
}

export const QuestionSuggestion: FC<Props> = ({
  followUpQuestions,
  onClick,
  scrollToBottom,
}) => {
  const handleClick = (question: string) => {
    onClick({ role: 'user', content: question, id: null });
  };

  const suggestRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    suggestRef?.current?.clientHeight && scrollToBottom();
  }, [suggestRef?.current?.clientHeight]);

  return (
    <div
      ref={suggestRef}
      className="relative m-auto center flex flex-col gap-4 mt-4"
    >
      {followUpQuestions.map((question, index) => (
        <Box
          key={index}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <Button
            variant="outlined"
            size="small"
            className="border-[#0156AC] text-[#0156AC] rounded-xl font-[Montserrat] p-2"
            style={{ textTransform: 'none' }}
            onClick={() => handleClick(question)}
          >
            {question}
          </Button>
        </Box>
      ))}
    </div>
  );
};

export default QuestionSuggestion;
