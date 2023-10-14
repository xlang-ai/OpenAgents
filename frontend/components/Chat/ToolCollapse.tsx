import { FC, ReactNode, useContext, useEffect, useState } from 'react';

import HomeContext from '@/pages/api/home/home.context';

import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import {
  Collapse,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';

interface ToolCollapseProps {
  icon: ReactNode;
  toolName: string | undefined;
  content: ReactNode;
  pluginUsing: boolean;
}

export const ToolCollapse: FC<ToolCollapseProps> = ({
  icon,
  toolName,
  content,
  pluginUsing,
}) => {
  const {
    state: { selectedConversation, chat_id },
  } = useContext(HomeContext);

  const [open, setOpen] = useState<boolean>(false);
  const [userClicked, setUserClicked] = useState<boolean>(false);

  const handleClick = () => {
    setOpen(!open);
    setUserClicked(true);
  };

  useEffect(() => {
    if (!userClicked) {
      setOpen(false);
    }
  }, [selectedConversation, chat_id]);

  return (
    <div>
      <ListItemButton
        onClick={handleClick}
        className="h-10 rounded-xl bg-[#f2f2f2] my-2 w-full"
      >
        <ListItemIcon className="min-w-[30px]">{icon}</ListItemIcon>
        <ListItemText>
          {pluginUsing ? (
            <div className="flex relative font-[Montserrat]">
              <div className="mt-1 ml-2">
                Using
                <span className="font-bold">{' ' + toolName}</span>
              </div>
              <div className="mt-[6px] ml-3 h-4 w-4 animate-spin rounded-full border-t-2 border-neutral-800 opacity-60"></div>
              <span className="absolute top-[5px] right-1 text-sm">
                {open ? 'Hide work' : 'Show work'}
              </span>
            </div>
          ) : (
            <div className="flex relative font-[Montserrat]">
              <div className="mt-1 ml-2">
                Used
                <span className="font-bold">{' ' + toolName}</span>
              </div>
              <span className="absolute top-[5px] right-1 text-sm">
                {open ? 'Hide work' : 'Show work'}
              </span>
            </div>
          )}
        </ListItemText>
        <div className="mt-1">{open ? <ExpandLess /> : <ExpandMore />}</div>
      </ListItemButton>
      <Collapse in={open} timeout="auto" unmountOnExit>
        {content}
      </Collapse>
    </div>
  );
};
