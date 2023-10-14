import React from 'react';

import FolderRoundedIcon from '@mui/icons-material/FolderRounded';
import InsertDriveFileRoundedIcon from '@mui/icons-material/InsertDriveFileRounded';

type Props = {
  droppable: boolean;
  fileType?: string;
};

export const TypeIcon: React.FC<Props> = (props) => {
  return props.droppable ? (
    <FolderRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
  ) : (
    <InsertDriveFileRoundedIcon sx={{ color: 'white', fontSize: 18 }} />
  );
};
