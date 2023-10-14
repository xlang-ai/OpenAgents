import React, { useEffect, useMemo, useRef, useState } from 'react';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

export const DndProviderWrapper: React.FC<any> = ({ className, children }) => {
  const context = useRef(null);
  //Make the dndAre a part of the component state otherwise, some times, the content doesn't renders
  const [dndArea, setDnDArea] = useState(context.current);
  //additionally, add a useEffect to track the context reference => might be overkill performance wise but works for my use case
  useEffect(() => {
    setDnDArea(context?.current);
  }, [context]);
  const html5Options = useMemo(() => ({ rootElement: dndArea }), [dndArea]);
  return (
    <div className={className} ref={context}>
      {/* it is important that DndProvider don't render if dndArea is null */}
      {dndArea && (
        <DndProvider backend={HTML5Backend} options={html5Options}>
          {children}
        </DndProvider>
      )}
    </div>
  );
};
