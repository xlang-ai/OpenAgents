import React, { FC, memo, useEffect, useState } from 'react';

import { KaggleSearchItem } from '@/types/kaggle';

import KaggleDatasetListItem from '@/components/Datatype/List/KaggleDatasetListItem';

import Grid from '@mui/material/Grid';

const data = Array.from({ length: 23 }).map((_, i) => ({
  href: 'https://ant.design',
  title: `COVID-19 effect on Liver Cancer Prediction Dataset`,
  avatar: `https://xsgames.co/randomusers/avatar.php?g=pixel&key=${i}`,
  description:
    'Predict the full impact of the COVID-19 on patients with primary liver cancer',
  content:
    'We supply a series of design principles, practical patterns and high quality design resources (Sketch and Axure), to help people create their product prototypes beautifully and efficiently.',
}));

interface Props {
  content: string;
}

const KaggleDatasetList: FC<Props> = memo(({ content }) => {
  const [searchResults, setSearchResults] = useState<KaggleSearchItem[]>([]);

  useEffect(() => {
    try {
      const data = JSON.parse(content);
      const items = data.map((item: any, index: number) => {
        return {
          id: item['id'],
          title: item['title'],
          image: item['cover_image_url'],
          description: item['subtitle'],
          likes: item['total_votes'],
          downloads: item['total_downloads'],
          href: item['url'],
        };
      });
      setSearchResults(items);
    } catch {
      setSearchResults([]);
    }
  }, [content]);

  return (
    <Grid container columnSpacing={1.5}>
      {searchResults.map((item) => (
        <Grid item xs={6}>
          <KaggleDatasetListItem item={item} />
        </Grid>
      ))}
    </Grid>
  );
});

export default KaggleDatasetList;
