import { IconFileExport, IconFileText, IconKey } from '@tabler/icons-react';
import { IconPlus } from '@tabler/icons-react';
import { useContext, useEffect, useRef, useState } from 'react';
import toast from 'react-hot-toast';

import { useTranslation } from 'next-i18next';

import { API_CREATE_FILE_FOLDER } from '@/utils/app/const';
import dataURLToBlob, {
  MAX_FILE_UPLOAD_SIZE,
  MAX_FILE_UPLOAD_SIZE_STRING,
} from '@/utils/app/upload';

import HomeContext from '@/pages/api/home/home.context';

import DraggleFolderTabContent from '@/components/Actionbar/TabContent/DraggableFolder';
import { DndProviderWrapper } from '@/components/Actionbar/TabContent/DraggableTreeItem/DndWrapper';

import Search from '../../Search';
import ChatbarContext from '../Chatbar.context';
import { ClearConversations } from './ClearConversations';

import CreateNewFolderRoundedIcon from '@mui/icons-material/CreateNewFolderRounded';
import PersonIcon from '@mui/icons-material/Person';
import {
  Button,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
} from '@mui/material';
import Dialog from '@mui/material/Dialog';

interface Props<T> {
  searchTerm: string;
  handleSearchTerm: (searchTerm: string) => void;
}

export const ChatbarSettings = <T,>({
  searchTerm,
  handleSearchTerm,
}: Props<T>) => {
  const { t } = useTranslation('sidebar');

  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [fileNames, setFileNames] = useState<string[]>([]);

  const menuRef = useRef<HTMLDivElement | null>(null);
  const buttonRef = useRef<HTMLButtonElement | null>(null);

  const openaiKey = useRef<HTMLInputElement | null>(null);
  const anthropicKey = useRef<HTMLInputElement | null>(null);

  const {
    state: {
      apiKey,
      chat_id,
      fileUploadProgress,
      files,
      isFileUpload,
      showAPIKeyModal,
    },
    dispatch: homeDispatch,
    handleUploadFileToServer,
    handleFetchDataPath,
  } = useContext(HomeContext);

  const { handleClearConversations, handleExportData } =
    useContext(ChatbarContext);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleCreateFolder = async (chat_id: string) => {
    let response;
    try {
      response = await fetch(API_CREATE_FILE_FOLDER, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chat_id: chat_id,
        }),
      });
    } catch (error: unknown) {
      toast.error((error as Error).message);
      return;
    }
    if (!response.ok) {
      toast.error(response.statusText);
      return;
    }

    const data = await response.json();
    if (!data || data['success'] === false) {
      toast.error('Error creating folder!');
      return;
    }
    handleFetchDataPath(chat_id, []);
  };

  const handleUpload = () => {
    if (!fileInputRef.current?.files?.length) return;
    const file_to_upload = fileInputRef.current.files[0];
    if (!file_to_upload) {
      toast.error('File cannot be uploaded');
      return;
    }

    // Limit upload file size
    if (file_to_upload.size > MAX_FILE_UPLOAD_SIZE) {
      toast.error(
        `File size should not exceed ${MAX_FILE_UPLOAD_SIZE_STRING}.`,
      );
      return;
    }

    // Existing files
    if (fileNames.includes(file_to_upload.name)) {
      if (!window.confirm('File already exists. Replace it?')) return;
    }

    const reader = new FileReader();

    reader.onload = async (e) => {
      try {
        const fileContents = e.target?.result as string;
        const blob = dataURLToBlob(fileContents);
        const file = new File([blob], file_to_upload.name);
        await handleUploadFileToServer(file, chat_id);
      } catch (e: any) {
        toast.error(`${e}`);
        return;
      }
    };

    reader.readAsDataURL(file_to_upload);

    fileInputRef.current.files = null;
  };

  const handleChangeAPIKey = async () => {
    const newAPIKey = {
      openai: openaiKey.current?.value || '',
      anthropic: anthropicKey.current?.value || '',
    };

    homeDispatch({ field: 'apiKey', value: newAPIKey });
    localStorage.setItem('openaiKey', newAPIKey.openai);
    localStorage.setItem('anthropicKey', newAPIKey.anthropic);

    const curDate = new Date();
    const expireDate = curDate.setTime(
      curDate.getTime() + 30 * 24 * 60 * 60 * 1000,
    );
    document.cookie = `openaiKey=${newAPIKey.openai}; expires=${expireDate}; path=/`;
    document.cookie = `anthropicKey=${newAPIKey.anthropic}; expires=${expireDate}; path=/`;

    homeDispatch({ field: 'showAPIKeyModal', value: false });
  };

  useEffect(() => {
    if (!isFileUpload && fileUploadProgress > 0) {
      toast.error('File upload failed!', {
        id: 'loading',
      });
    }
    if (isFileUpload) {
      toast.loading(
        `File uploading... ${(fileUploadProgress * 100).toFixed(2)}%`,
        {
          id: 'loading',
        },
      );
      if (Math.abs(fileUploadProgress - 1) < 0.000001) {
        toast.success('File uploaded successfully!', {
          id: 'loading',
        });
        homeDispatch({ field: 'isFileUpload', value: false });
        homeDispatch({ field: 'fileUploadProgress', value: 0 });
        homeDispatch({ field: 'messageIsStreaming', value: false });
      }
    }
  }, [isFileUpload, fileUploadProgress]);

  useEffect(() => {
    let curFileNames: string[] = [];
    files.forEach((file) => {
      if (file.parent == 0) curFileNames.push(file.text);
    });
    setFileNames(curFileNames);
  }, [files]);

  // click outside to close menu
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(e.target as Node) &&
        buttonRef.current &&
        !buttonRef.current.contains(e.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, setIsOpen, menuRef, buttonRef]);

  return (
    <>
      <div className="flex flex-col space-y-1 border-t border-white/50 pt-1 text-sm">
        <span className="pl-3 pt-1 text-white font-[500] text-lg">Files</span>
        <Search
          placeholder="Search File"
          searchTerm={searchTerm}
          onSearch={handleSearchTerm}
        />
        <div className="m-auto flex flex-col gap-2 w-full mb-2 mt-2 pt-1 h-[200px] flex-grow overflow-auto">
          <DndProviderWrapper className="draggle-folder">
            <DraggleFolderTabContent />
          </DndProviderWrapper>
        </div>
        <div className="flex items-center mb-1 mt-1 justify-center">
          <input
            id="upload-file"
            className="sr-only"
            tabIndex={-1}
            type="file"
            accept=".csv, .tsv, .xslx, .db, .sqlite, .png, .jpg, .jpeg"
            ref={fileInputRef}
            onChange={handleUpload}
          />
          <button
            className="text-sidebar flex w-[200px] flex-shrink-0 cursor-pointer select-none items-center justify-center 
              gap-2 rounded-xl p-2 text-white bg-[#4B2E83] font-[600]"
            onClick={() => {
              fileInputRef.current?.click();
            }}
          >
            <IconPlus size={16} />
            {t('Upload')}
          </button>

          <button
            className="ml-2 flex flex-shrink-0 cursor-pointer items-center gap-2 rounded-xl p-2 text-sm text-white bg-[#7A7A7A]"
            onClick={() => {
              handleCreateFolder(chat_id);
            }}
          >
            <CreateNewFolderRoundedIcon sx={{ color: 'white', fontSize: 20 }} />
          </button>
        </div>
      </div>
      <div className="flex flex-col items-center space-y-1 border-t border-white/20 pt-1 text-sm">
        <div className="w-full relative">
          {isOpen && (
            <div
              className="absolute bottom-full left-0 z-20 mb-2 w-full overflow-hidden rounded-md bg-[#050509] py-1.5 outline-none"
              role="menu"
              ref={menuRef}
            >
              <MenuButton
                onClick={() => {
                  homeDispatch({ field: 'showTerms', value: true });
                }}
                icon={<IconFileText className="w-4 h-4" />}
                text={t('Terms of Use') as string}
              />
              <div className="my-1.5 h-px bg-white/20" role="none"></div>
              <ClearConversations
                onClearConversations={handleClearConversations}
                closeMenu={() => setIsOpen(false)}
              />
              <MenuButton
                text={t('Export Data') as string}
                icon={<IconFileExport size={18} />}
                onClick={() => handleExportData()}
              />
              <MenuButton
                text={t('API Keys') as string}
                icon={<IconKey size={18} />}
                onClick={() =>
                  homeDispatch({ field: 'showAPIKeyModal', value: true })
                }
              />
              <div className="my-1.5 h-px bg-white/20" role="none"></div>
            </div>
          )}
        </div>
      </div>

      <Dialog open={showAPIKeyModal}>
        <DialogTitle className="font-[Montserrat]">
          Set Your Own API Keys
        </DialogTitle>
        <DialogContent>
          <div className="flex">
            <span className="font-[Montserrat]">OpenAI: </span>
            <input
              ref={openaiKey}
              defaultValue={apiKey.openai}
              className="ml-7 border w-[50rem]"
            />
          </div>
          <div className="flex mt-4">
            <span className="font-[Montserrat]">Anthropic: </span>
            <input
              ref={anthropicKey}
              defaultValue={apiKey.anthropic}
              className="ml-2 border w-[50rem]"
            />
          </div>
          <div className="flex mt-4">
            <span className="font-[Montserrat] font-[600]">Note:&nbsp;</span>
            <div className="font-[Montserrat]">
              Your API keys will only be stored in your{' '}
              <span className="font-[Montserrat] font-[600]">local</span>{' '}
              client.
            </div>
          </div>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleChangeAPIKey}>Submit</Button>
          <Button
            onClick={() =>
              homeDispatch({ field: 'showAPIKeyModal', value: false })
            }
          >
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export const MenuButton = ({
  icon,
  href,
  text,
  onClick,
}: {
  icon?: React.ReactElement;
  href?: string;
  text?: string;
  onClick?: () => void;
}) => {
  return (
    <a
      href={href}
      target={href && '_blank'}
      className="flex py-3 px-3 items-center gap-3 transition-colors duration-200 text-white cursor-pointer hover:bg-[#40414f]"
      onClick={onClick}
    >
      {icon}
      {text}
    </a>
  );
};
