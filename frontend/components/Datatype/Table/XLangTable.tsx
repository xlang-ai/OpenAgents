import MaterialReactTable from 'material-react-table';
import React, { FC, memo, useEffect, useState } from 'react';

interface Props {
  content: string;
}
const XLangTable: FC<Props> = memo(({ content }) => {
  const [data, setData] = useState([]);
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    const table = JSON.parse(content);
    setColumns(table.columns);
    setData(table.data);
  }, []);

  return (
    <MaterialReactTable
      columns={columns}
      data={data}
      enableColumnResizing
      initialState={{ density: 'compact' }}
      enableBottomToolbar={true}
      muiBottomToolbarProps={{
        sx: {
          zIndex: 0,
        },
      }}
      muiTableContainerProps={{
        className: 'px-5',
      }}
    />
  );
});

export default XLangTable;
