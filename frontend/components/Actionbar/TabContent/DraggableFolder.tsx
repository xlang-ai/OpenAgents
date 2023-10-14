import {
  DropOptions,
  NodeModel,
  Tree,
  isAncestor,
} from '@minoru/react-dnd-treeview';
import React, { useContext, useEffect, useRef, useState } from 'react';

import { FileItem } from '@/types/files';

import HomeContext from '@/pages/api/home/home.context';

import ChatbarContext from '@/components/Chatbar/Chatbar.context';

import styles from './DraggableTreeItem/App.module.css';
import { CustomDragPreview } from './DraggableTreeItem/CustomDragPreview';
import { CustomNode } from './DraggableTreeItem/CustomNode';
import { MultipleDragPreview } from './DraggableTreeItem/MultipleDragPreview';
import { theme } from './DraggableTreeItem/theme';

import { CssBaseline, ThemeProvider } from '@mui/material';

const DraggleFolderTabContent = () => {
  const {
    state: { chat_id },
    handleFetchDataPath,
    handleMoveFiles,
  } = useContext(HomeContext);

  const {
    state: { filteredFiles },
  } = useContext(ChatbarContext);

  const [tree, setTree] = useState(filteredFiles);
  const [selectedNodes, setSelectedNodes] = useState<NodeModel<FileItem>[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isCtrlPressing, setIsCtrlPressing] = useState(false);
  const [curFocusNodeID, setCurFocusNodeID] = useState<string | number>(0);

  useEffect(() => {
    setTree(filteredFiles);
  }, [filteredFiles]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent): any => {
      if (e.key.toLowerCase() === 'escape') {
        setSelectedNodes([]);
      } else if (e.ctrlKey || e.metaKey) {
        setIsCtrlPressing(true);
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'control' || e.key.toLowerCase() === 'meta') {
        setIsCtrlPressing(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  const handleSingleSelect = (node: NodeModel<FileItem>) => {
    const selectedIds = selectedNodes.map((n) => n.id);
    if (selectedIds.includes(node.id)) setSelectedNodes([]);
    else setSelectedNodes([node]);
  };

  const handleMultiSelect = (clickedNode: NodeModel<FileItem>) => {
    const selectedIds = selectedNodes.map((n) => n.id);

    // ignore if the clicked node is already selected
    if (selectedIds.includes(clickedNode.id)) {
      const removedUpdatedNotes = selectedNodes.filter(
        (n) => n.id !== clickedNode.id,
      );
      setSelectedNodes(removedUpdatedNotes);
      return;
    }

    // ignore if ancestor node already selected
    if (
      selectedIds.some((selectedId) =>
        isAncestor(tree, selectedId, clickedNode.id),
      )
    ) {
      return;
    }

    let updateNodes = [...selectedNodes];

    // if descendant nodes already selected, remove them
    updateNodes = updateNodes.filter((selectedNode) => {
      return !isAncestor(tree, clickedNode.id, selectedNode.id);
    });

    updateNodes = [...updateNodes, clickedNode];
    setSelectedNodes(updateNodes);
  };

  const handleClick = (e: React.MouseEvent, node: NodeModel<FileItem>) => {
    if (e.ctrlKey || e.metaKey) {
      handleMultiSelect(node);
    } else {
      handleSingleSelect(node);
    }
    setCurFocusNodeID(node.id);
  };

  const handleDragStart = (node: NodeModel<FileItem>) => {
    const isSelectedNode = selectedNodes.some((n) => n.id === node.id);
    setIsDragging(true);

    if (!isCtrlPressing && isSelectedNode) {
      return;
    }

    if (!isCtrlPressing) {
      setSelectedNodes([node]);
      return;
    }

    if (!selectedNodes.some((n) => n.id === node.id)) {
      setSelectedNodes([...selectedNodes, node]);
    }
  };

  const handleDragEnd = () => {
    setIsDragging(false);
    setIsCtrlPressing(false);
    setSelectedNodes([]);
  };

  const handleDrop = async (
    newTree: NodeModel<FileItem>[],
    options: DropOptions,
  ) => {
    const { dropTargetId } = options;
    const nodeToUpdate: FileItem[] = [];
    const updateTree = newTree.map((node) => {
      if (selectedNodes.some((selectedNode) => selectedNode.id === node.id)) {
        nodeToUpdate.push(node as FileItem);
        return {
          ...node,
          parent: dropTargetId,
          id: node.id,
        };
      }
      return node;
    });

    const moveResult = await handleMoveFiles(chat_id, nodeToUpdate);
    if (!moveResult) return;

    handleFetchDataPath(chat_id, []);

    setTree(updateTree as FileItem[]);
    setSelectedNodes([]);
  };

  useEffect(() => {
    const controller = new AbortController();
    handleFetchDataPath(chat_id, []);
    return () => {
      controller.abort();
    };
  }, [chat_id]);

  const folderAreaRef = useRef<HTMLDivElement>(null);
  // click outside to close menu
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        folderAreaRef.current &&
        !folderAreaRef.current.contains(e.target as Node)
      ) {
        setSelectedNodes([]);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="text-white">
        <div className={styles.storyRoot} ref={folderAreaRef}>
          <Tree
            rootId={0}
            tree={tree}
            classes={{
              root: `${styles.treeRoot} w-full truncate`,
              dropTarget: styles.dropTarget,
              listItem: 'rounded-lg',
            }}
            onDrop={handleDrop}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            canDrop={(tree, options) => {
              if (
                selectedNodes.some(
                  (selectedNode) => selectedNode.id === options.dropTargetId,
                )
              ) {
                return false;
              }
            }}
            render={(node, options) => {
              const selected = selectedNodes.some(
                (selectedNode) => selectedNode.id === node.id,
              );
              const isShowOptions =
                selectedNodes[selectedNodes.length - 1]?.id === node.id;
              return (
                <CustomNode
                  node={node}
                  {...options}
                  isSelected={selected}
                  isDragging={selected && isDragging}
                  onClick={handleClick}
                  curFocusNodeID={curFocusNodeID}
                  isShowOptions={isShowOptions}
                  unSelect={() => setSelectedNodes([])}
                />
              );
            }}
            dragPreviewRender={(monitorProps) => {
              if (selectedNodes.length > 1) {
                return <MultipleDragPreview dragSources={selectedNodes} />;
              }

              return <CustomDragPreview monitorProps={monitorProps} />;
            }}
          />
        </div>
      </div>
    </ThemeProvider>
  );
};

export default DraggleFolderTabContent;
