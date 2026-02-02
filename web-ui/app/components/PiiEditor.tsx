'use client';

import React, { useState, useEffect } from 'react';
import { PiiEntity, PiiResponse } from '../types';
import PiiHighlighter from './PiiHighlighter';

const PiiEditor: React.FC = () => {
  const [text, setText] = useState<string>('');
  const [entities, setEntities] = useState<PiiEntity[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [lastProcessedTime, setLastProcessedTime] = useState<number | null>(null);

  // Debounce logic: Wait 1s after typing stops to call API
  useEffect(() => {
    const handler = setTimeout(() => {
      if (text.trim().length > 0) {
        detectPii(text);
      } else {
        setEntities([]);
        setLastProcessedTime(null);
      }
    }, 1000);

    return () => {
      clearTimeout(handler);
    };
  }, [text]);

  const detectPii = async (inputText: string) => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!res.ok) {
        throw new Error('Failed to detect PII');
      }

      const data: PiiResponse = await res.json();
      setEntities(data.entities);
      setLastProcessedTime(data.processing_time);
    } catch (error) {
      console.error('Error detecting PII:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-4">
      {/* Input Section */}
      <div className="flex flex-col gap-2">
        <label className="font-semibold text-gray-700">Raw Input</label>
        <textarea
          className="w-full h-96 p-4 border rounded shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none font-mono text-sm resize-none"
          placeholder="Paste text here to detect PII (e.g., emails, phone numbers)..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <div className="text-xs text-gray-500 text-right">
          {text.length} characters
        </div>
      </div>

      {/* Output Section */}
      <div className="flex flex-col gap-2">
        <div className="flex justify-between items-center">
          <label className="font-semibold text-gray-700">Live PII Detection</label>
          {isLoading && <span className="text-xs text-blue-600 animate-pulse">Analyzing...</span>}
          {!isLoading && lastProcessedTime && (
            <span className="text-xs text-green-600">
              Processed in {lastProcessedTime.toFixed(3)}s
            </span>
          )}
        </div>
        
        {/* The Highlighter View */}
        <div className="h-96 overflow-y-auto border rounded shadow-sm bg-gray-50">
          <PiiHighlighter text={text} entities={entities} />
        </div>
        
        <div className="text-xs text-gray-500">
          Hover over highlights to see PII type.
        </div>
      </div>
    </div>
  );
};

export default PiiEditor;
