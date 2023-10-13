import React from 'react';

import LogoIconImage from './logo_color.svg';

const LogoIcon = (props: React.HTMLProps<HTMLImageElement>) => {
  return <img src={LogoIconImage.src} alt="Logo Icon" {...props} />;
};

export default LogoIcon;