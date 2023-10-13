import { IconX } from '@tabler/icons-react';
import { FC } from 'react';

import { useTranslation } from 'next-i18next';

import SearchIcon from '@mui/icons-material/Search';
import IconButton from '@mui/material/IconButton';

interface Props {
  placeholder: string;
  searchTerm: string;
  onSearch: (searchTerm: string) => void;
}
const Search: FC<Props> = ({ placeholder, searchTerm, onSearch }) => {
  const { t } = useTranslation('sidebar');

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onSearch(e.target.value);
  };

  const clearSearch = () => {
    onSearch('');
  };

  return (
    <div className="relative flex items-center justify-center pt-1 px-3">
      <input
        className="w-full flex-1 h-[35px] rounded-xl font-[500] font-[Montserrat] border border-white/50 
          bg-[transparent] px-4 py-3 text-[13px] leading-3 border-[#D8D8D8] text-[#D8D8D8] placeholder:text-[#D8D8D8]"
        type="text"
        placeholder={t(placeholder) || ''}
        value={searchTerm}
        onChange={handleSearchChange}
      />
      <IconButton
        type="button"
        className="absolute right-2 text-[#D8D8D8]"
        aria-label="search"
      >
        <SearchIcon />
      </IconButton>
      {searchTerm && (
        <IconX
          className="absolute right-10 cursor-pointer text-[#D8D8D8] text-neutral-300 hover:text-neutral-400"
          size={18}
          onClick={clearSearch}
        />
      )}
    </div>
  );
};

export default Search;
