import React from 'react';

import RobotIconImage from './logo_rect.svg';

const RobotIcon = (props: React.HTMLProps<HTMLImageElement>) => {
  return <img src={RobotIconImage.src} alt="Robot Icon" {...props} />;
};

export default RobotIcon;