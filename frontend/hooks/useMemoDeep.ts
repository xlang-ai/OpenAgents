import React, { useEffect, useRef } from 'react';

import isEqual from 'lodash/isEqual';

const useMemoDeep = <T>(factory: () => T, dependencies: any[]): T => {
  const memoizedValue = useRef<T | null>(null);
  const prevDependencies = useRef<any[]>([]);

  if (!isEqual(dependencies, prevDependencies.current)) {
    memoizedValue.current = factory();
    prevDependencies.current = dependencies;
  }

  return memoizedValue.current!;
};

export default useMemoDeep;
