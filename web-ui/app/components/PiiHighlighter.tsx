import React from 'react';
import { PiiEntity } from '../types';

interface PiiHighlighterProps {
  text: string;
  entities: PiiEntity[];
}

const PiiHighlighter: React.FC<PiiHighlighterProps> = ({ text, entities }) => {
  if (!entities || entities.length === 0) {
    return <p className="whitespace-pre-wrap text-gray-800">{text}</p>;
  }

  // Sort entities by start index to ensure correct processing
  const sortedEntities = [...entities].sort((a, b) => a.start - b.start);

  const parts = [];
  let lastIndex = 0;

  sortedEntities.forEach((entity, index) => {
    // Add non-highlighted text before the entity
    if (entity.start > lastIndex) {
      parts.push(
        <span key={`text-${index}`}>
          {text.slice(lastIndex, entity.start)}
        </span>
      );
    }

    // Add highlighted entity
    parts.push(
      <span
        key={`entity-${index}`}
        className="bg-yellow-200 text-yellow-800 px-1 rounded border border-yellow-300 relative group cursor-help"
        title={entity.label}
      >
        {text.slice(entity.start, entity.end)}
        <span className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 hidden group-hover:block bg-gray-900 text-white text-xs rounded py-1 px-2 z-10 whitespace-nowrap">
          {entity.label}
        </span>
      </span>
    );

    lastIndex = entity.end;
  });

  // Add remaining text
  if (lastIndex < text.length) {
    parts.push(<span key="text-remaining">{text.slice(lastIndex)}</span>);
  }

  return (
    <div className="p-4 bg-white border rounded shadow-sm min-h-[150px] whitespace-pre-wrap font-mono text-sm leading-relaxed">
      {parts}
    </div>
  );
};

export default PiiHighlighter;
