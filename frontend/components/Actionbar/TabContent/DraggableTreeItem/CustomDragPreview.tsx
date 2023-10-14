import { DragLayerMonitorProps } from '@minoru/react-dnd-treeview';
import React from 'react';

import { FileItem } from '@/types/files';

import styles from './CustomDragPreview.module.css';
import { TypeIcon } from './TypeIcon';

export const CustomDragPreview = ({
  monitorProps,
}: {
  monitorProps: DragLayerMonitorProps<FileItem>;
}) => {
  const item = monitorProps.item;

  return (
    <div className={styles.root}>
      <div className={styles.icon}>
        <TypeIcon
          droppable={item.droppable ?? false}
          fileType={item?.data?.fileType}
        />
      </div>
      <div className={styles.label}>{item.text}</div>
    </div>
  );
};
