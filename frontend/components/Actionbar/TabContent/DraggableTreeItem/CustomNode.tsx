import React, {
  KeyboardEvent,
  MouseEventHandler,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react';

import { FileItem } from '@/types/files';

import HomeContext from '@/pages/api/home/home.context';

import SidebarActionButton from '@/components/Buttons/SidebarActionButton';

import styles from './CustomNode.module.css';
import { TypeIcon } from './TypeIcon';

import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import AttachFileRoundedIcon from '@mui/icons-material/AttachFileRounded';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import DownloadRoundedIcon from '@mui/icons-material/DownloadRounded';
import EditRoundedIcon from '@mui/icons-material/EditRounded';
import { Tour, TourProps } from 'antd';

export const CustomNode = ({ testIdPrefix = '', ...props }) => {
  const {
    state: { chat_id, selectedConversation, selectedCodeInterpreterPlugins },
    handleUpdateFile,
    handleDeleteFile,
    handleFetchDataPath,
    handleApplyFileToConversation,
    handleDownloadFile,
    handleSend: _handleSend,
  } = useContext(HomeContext);

  const { id, droppable, data } = props.node;
  const indent = props.depth * 24;

  const [isDeleting, setIsDeleting] = useState(false);
  const [isRenaming, setIsRenaming] = useState(false);
  const [isApplying, setIsApplying] = useState(false);
  const [renameValue, setRenameValue] = useState('');
  const [isGeneratingDataSummary, setIsGeneratingDataSummary] = useState(false);

  const handleClick = (e: React.MouseEvent) => {
    props.onClick(e, props.node);
  };

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    props.onToggle();
  };

  if (props.isSelected) {
    props.containerRef.current?.classList.add(styles.selected);
  } else {
    props.containerRef.current?.classList.remove(styles.selected);
  }

  if (props.isDragging) {
    props.containerRef.current?.classList.add(styles.dragging);
  } else {
    props.containerRef.current?.classList.remove(styles.dragging);
  }

  const handleOpenRenameModal: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.stopPropagation();
    setIsRenaming(true);
    props.isSelected && setRenameValue(props.node.text);
  };
  const handleOpenDeleteModal: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.stopPropagation();
    setIsDeleting(true);
  };
  const handleOpenApplyModal: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.stopPropagation();
    setIsApplying(true);
  };

  const handleConfirm: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.stopPropagation();
    if (isDeleting) {
      handleDeleteFile(chat_id, props.node);
    } else if (isRenaming) {
      handleRename(props.node);
    } else if (isApplying) {
      handleApply(props.node);
    }
    setIsDeleting(false);
    setIsRenaming(false);
    setIsApplying(false);
    props.unSelect();
  };

  const handleCancel: MouseEventHandler<HTMLButtonElement> = (e) => {
    e.stopPropagation();
    setIsDeleting(false);
    setIsRenaming(false);
    setIsApplying(false);
    props.unSelect();
  };

  const handleSendMessage = useCallback(_handleSend, [selectedConversation]);

  const handleApply = async (node: FileItem) => {
    const setting = await handleApplyFileToConversation(chat_id, node);
    const isEnableDataProfiling = selectedCodeInterpreterPlugins.some(
      (tool) => tool.nameForHuman === 'Data Profiling',
    );
    setIsGeneratingDataSummary(setting && isEnableDataProfiling);
  };

  useEffect(() => {
    (async () => {
      if (isGeneratingDataSummary) {
        setIsGeneratingDataSummary(false);
        if (selectedConversation) {
          let parent_message_id: number | null = -1;
          if (selectedConversation.messages?.length > 0) {
            parent_message_id =
              selectedConversation.messages[
                selectedConversation.messages.length - 1
              ].id;
          }
          await handleSendMessage(
            {
              role: 'user',
              content: '',
              type: '',
              richContent: null,
              id: null,
              apiType: 'DataProfiling',
            },
            0,
            false,
            null,
            {
              api_name: 'DataProfiling',
              args: {
                activated_file: props.node,
                chat_id: selectedConversation.id,
                parent_message_id: parent_message_id,
              },
            },
          );
        }
      }
    })();
  }, [selectedConversation]);

  const handleRename = async (node: FileItem) => {
    if (renameValue.trim().length > 0 && node) {
      await handleUpdateFile(chat_id, node, renameValue);
      setRenameValue('');
      setIsRenaming(false);
      props.node.text = renameValue;
      handleFetchDataPath(chat_id, []);
      props.unSelect();
    }
  };

  const handleDownload = async () => {
    const blob = await handleDownloadFile(props.node);
    if (blob) {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = props.node.text;
      a.click();
      window.URL.revokeObjectURL(url);
    }
    props.unSelect();
  };

  const handleEnterDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      props.isSelected && handleRename(props.node);
    }
  };

  const ref = useRef<HTMLDivElement>(null);
  const [openTour, setOpenTour] = useState(true);
  const [steps, setSteps] = useState<TourProps['steps']>([]);

  useEffect(() => {
    setSteps([
      {
        title: 'New Dataset Downloaded',
        description:
          'You can import the dataset ' +
          props.node.text +
          ' into the conversation by clicking the apply button.',
        target: () => ref.current!,
        type: 'primary',
      },
    ]);
  }, [props.node]);

  useEffect(() => {
    setIsDeleting(false);
    setIsRenaming(false);
    setIsApplying(false);
  }, [props.isSelected]);

  return (
    <>
      <div
        className={`${styles.root} w-full rounded-lg`}
        style={{ paddingInlineStart: indent }}
        data-testid={`${testIdPrefix}custom-node-${id}`}
        onClick={handleClick}
        ref={ref}
      >
        <div className={`${styles.arrow} ${props.isOpen ? styles.isOpen : ''}`}>
          {props.node.droppable &&
            (props.isOpen ? (
              <div onClick={handleToggle}>
                <ArrowDropDownIcon
                  sx={{ color: 'white' }}
                  data-testid={`arrow-down-icon-${id}`}
                />
              </div>
            ) : (
              <div onClick={handleToggle}>
                <ArrowRightIcon
                  sx={{ color: 'white' }}
                  data-testid={`arrow-right-icon-${id}`}
                />
              </div>
            ))}
        </div>
        <div className={styles.filetype}>
          <TypeIcon droppable={droppable || false} fileType={data?.fileType} />
        </div>

        {isRenaming ? (
          <input
            className="relative flex-1 border-neutral-400 pl-2 w-full bg-transparent text-left leading-3 text-white outline-none"
            type="text"
            value={renameValue}
            onChange={(e) => setRenameValue(e.target.value)}
            onKeyDown={handleEnterDown}
            autoFocus
          />
        ) : (
          <button
            className={`flex-1 w-full cursor-pointer gap-2 rounded-lg p-2 text-sm transition-colors duration-200 truncate`}
          >
            <div
              className={
                'relative max-h-5 flex-1 overflow-hidden text-ellipsis whitespace-nowrap break-all text-left pr-1 truncate'
              }
            >
              {props.node.text}
            </div>
          </button>
        )}

        {(isDeleting || isRenaming || isApplying) &&
          props.curFocusNodeID == props.node.id && (
            <div className="flex text-gray-300">
              <SidebarActionButton handleClick={handleConfirm} title="Confirm">
                <CheckRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
              </SidebarActionButton>
              <SidebarActionButton handleClick={handleCancel} title="Cancel">
                <CloseRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
              </SidebarActionButton>
            </div>
          )}

        {props.isSelected &&
          props.isShowOptions &&
          !isRenaming &&
          !isDeleting &&
          !isApplying && (
            <div className="flex text-gray-300">
              {!props.node.droppable && (
                <SidebarActionButton
                  handleClick={handleOpenApplyModal}
                  title="Apply"
                >
                  <AttachFileRoundedIcon
                    sx={{ color: 'white', fontSize: 18 }}
                  />
                </SidebarActionButton>
              )}
              {props.node.droppable && (
                <SidebarActionButton
                  handleClick={handleOpenRenameModal}
                  title="Rename"
                >
                  <EditRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
                </SidebarActionButton>
              )}
              {!props.node.droppable && (
                <SidebarActionButton
                  handleClick={handleDownload}
                  title="Download"
                >
                  <DownloadRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
                </SidebarActionButton>
              )}
              <SidebarActionButton
                handleClick={handleOpenDeleteModal}
                title="Delete"
              >
                <DeleteRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
              </SidebarActionButton>
            </div>
          )}
      </div>
      {props.node.highlight && (
        <div className="text-black">
          <Tour
            open={openTour}
            onClose={() => setOpenTour(false)}
            steps={steps}
          />
        </div>
      )}
    </>
  );
};
