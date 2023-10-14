import { NodeModel } from '@minoru/react-dnd-treeview';
import React from 'react';

import { FileItem } from '@/types/files';

import styles from './MultipleDragPreview.module.css';
import { TypeIcon } from './TypeIcon';

import { Badge } from '@mui/material';

export const MultipleDragPreview = ({
  dragSources,
}: {
  dragSources: NodeModel<FileItem>[];
}) => {
  return (
    <Badge
      classes={{ badge: styles.badge }}
      color="error"
      badgeContent={dragSources.length}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <div className={styles.root} data-testid="custom-drag-preview">
        {dragSources.map((node) => (
          <div className={styles.item}>
            <div className={styles.icon}>
              <TypeIcon
                droppable={node.droppable || false}
                fileType={node?.data?.fileType}
              />
            </div>
            <div className={styles.label}>{node.text}</div>
          </div>
        ))}
      </div>
    </Badge>
  );
};
