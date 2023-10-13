import { IconArrowBarLeft, IconArrowBarRight } from '@tabler/icons-react';

interface Props {
  onClick: any;
  side: 'left' | 'right';
}

export const CloseSidebarButton = ({ onClick, side }: Props) => {
  return (
    <>
      <button className="pt-1 ml-[6rem]" onClick={onClick}>
        {side === 'right' ? <IconArrowBarRight /> : <IconArrowBarLeft />}
      </button>
    </>
  );
};

export const OpenSidebarButton = ({ onClick, side }: Props) => {
  return (
    <button className="fixed top-5 ml-[7.5rem] text-black" onClick={onClick}>
      {side === 'right' ? <IconArrowBarLeft /> : <IconArrowBarRight />}
    </button>
  );
};
