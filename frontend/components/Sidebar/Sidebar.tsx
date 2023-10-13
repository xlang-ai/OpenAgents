import { IconMistOff, IconPlus } from '@tabler/icons-react';
import { ReactNode, useContext } from 'react';
import { useTranslation } from 'react-i18next';

import HomeContext from '@/pages/api/home/home.context';

import {
  CloseSidebarButton,
  OpenSidebarButton,
} from './components/OpenCloseButton';

import Search from '../Search';

import LogoIcon from '@/icons/LogoIcon';
import CreateNewFolderRoundedIcon from '@mui/icons-material/CreateNewFolderRounded';
import PersonIcon from '@mui/icons-material/Person';

interface Props<T> {
  isOpen: boolean;
  addItemButtonTitle: string;
  side: 'left' | 'right';
  items: T[];
  itemComponent: ReactNode;
  folderComponent: ReactNode;
  footerComponent?: ReactNode;
  searchTerm: string;
  handleSearchTerm: (searchTerm: string) => void;
  toggleOpen: () => void;
  handleCreateItem: () => void;
  handleCreateFolder: () => void;
  handleDrop: (e: any) => void;
}

const Sidebar = <T,>({
  isOpen,
  addItemButtonTitle,
  side,
  items,
  itemComponent,
  folderComponent,
  footerComponent,
  searchTerm,
  handleSearchTerm,
  toggleOpen,
  handleCreateItem,
  handleCreateFolder,
  handleDrop,
}: Props<T>) => {
  const {
    state: { messageIsStreaming },
  } = useContext(HomeContext);

  const { t } = useTranslation('promptbar');

  const allowDrop = (e: any) => {
    e.preventDefault();
  };

  const highlightDrop = (e: any) => {
    e.target.style.background = '#343541';
  };

  const removeHighlight = (e: any) => {
    e.target.style.background = '';
  };

  const disableStyle: React.CSSProperties = messageIsStreaming
    ? {
        pointerEvents: 'none',
        cursor: 'not-allowed',
      }
    : {};

  return isOpen ? (
    <div style={disableStyle} className="bg-[#F3F3F3]">
      <div
        className={`fixed rounded-3xl rounded-l-none top-0 ${side}-0 z-40 flex h-full w-[260px] flex-none flex-col space-y-2 bg-[#031425] p-2 text-[13px] sm:relative sm:top-0`}
      >
        <div className="flex items-center leading-10 h-10 pt-1 pl-4">
          <a href="https://xlang.ai" target="_blank" rel="noreferrer">
            <LogoIcon className="fixed top-5 left-5 w-10" />
          </a>
          <span
            className="pl-12 pt-1"
            style={{
              color: '#FFF',
              fontFamily: 'Montserrat',
              fontSize: '17px',
              fontWeight: 400,
            }}
          >
            XLANG
          </span>
          <CloseSidebarButton onClick={toggleOpen} side={side} />
        </div>
        <span className="border-t border-white/50 pt-3 pl-3 text-white font-[500] text-lg">
          Chats
        </span>
        <Search
          placeholder="Search Chat"
          searchTerm={searchTerm}
          onSearch={handleSearchTerm}
        />
        <div className="flex-grow overflow-auto">
          {items?.length > 0 && <div className="flex">{folderComponent}</div>}

          {items?.length > 0 ? (
            <div
              onDrop={handleDrop}
              onDragOver={allowDrop}
              onDragEnter={highlightDrop}
              onDragLeave={removeHighlight}
            >
              {itemComponent}
            </div>
          ) : (
            <div className="mt-8 select-none text-center text-white">
              <IconMistOff className="mx-auto mb-3" />
              <span className="text-[14px] leading-normal">
                {t('No data.')}
              </span>
            </div>
          )}
        </div>
        <div className="flex items-center justify-center pb-1">
          <button
            className={`flex w-[200px] flex-shrink-0 cursor-pointer select-none items-center justify-center gap-2 bg-[#4B2E83]
             rounded-xl p-2 text-white font-[600]`}
            onClick={() => {
              handleCreateItem();
              handleSearchTerm('');
            }}
          >
            <IconPlus size={16} />
            {addItemButtonTitle}
          </button>
          <button
            className="ml-2 flex flex-shrink-0 cursor-pointer items-center gap-2 rounded-xl p-2 text-sm text-white bg-[#7A7A7A]"
            onClick={handleCreateFolder}
          >
            <CreateNewFolderRoundedIcon sx={{ color: 'white', fontSize: 20 }} />
          </button>
        </div>
        {footerComponent}
      </div>
    </div>
  ) : (
    <div
      className={`fixed justify-center rounded-3xl rounded-l-none top-0 ${side}-0 z-40 flex h-full w-[80px] bg-[#031425] text-[13px] sm:relative sm:top-0`}
    >
      <LogoIcon className="fixed top-5 left-5 w-10" />
      <OpenSidebarButton onClick={toggleOpen} side={side} />
      <div className="fixed bottom-5 w-10">
        <PersonIcon />
      </div>
    </div>
  );
};

export default Sidebar;
