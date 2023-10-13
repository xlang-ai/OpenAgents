export interface Files {
  id: string;
  name: string;
  children?: readonly Files[];
  parent?: string;
}

export interface FileItem {
  id: number;
  parent: number;
  droppable: boolean;
  text: string;
  fileType?: string;
}

export interface ExternalDataFile {
  id: string;
  name: string;
  type: ExternalDataFileType;
}

export type ExternalDataFileType = 'google' | 'snowflake' | 'tableau';
