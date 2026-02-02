'use client';

import React, { useEffect, useState } from 'react';
import { DocumentLog } from '../types';

const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentLog[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchDocuments = async () => {
    try {
      const res = await fetch('/api/documents');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    // Poll every 5 seconds to keep it live
    const interval = setInterval(fetchDocuments, 5000);
    return () => clearInterval(interval);
  }, []);

  if (isLoading && documents.length === 0) {
    return <div className="p-4 text-center text-gray-500">Loading audit logs...</div>;
  }

  return (
    <div className="bg-white rounded shadow-sm border overflow-hidden">
      <div className="p-4 border-b bg-gray-50 flex justify-between items-center">
        <h2 className="font-semibold text-gray-800">Audit Logs (Recent Scans)</h2>
        <span className="text-xs text-gray-500">Auto-refreshing every 5s</span>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead className="bg-gray-100 text-gray-600 uppercase text-xs font-medium">
            <tr>
              <th className="p-3">ID</th>
              <th className="p-3">Timestamp</th>
              <th className="p-3">Model</th>
              <th className="p-3">Latency</th>
              <th className="p-3">PII Detected</th>
              <th className="p-3 w-1/3">Snippet</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {documents.map((doc) => (
              <tr key={doc.id} className="hover:bg-gray-50 transition-colors">
                <td className="p-3 font-mono text-gray-500">#{doc.id}</td>
                <td className="p-3 text-gray-700">
                  {new Date(doc.created_at).toLocaleString()}
                </td>
                <td className="p-3">
                  <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                    {doc.model_used}
                  </span>
                </td>
                <td className="p-3 text-gray-600">
                  {doc.processing_time?.toFixed(3)}s
                </td>
                <td className="p-3">
                  {doc.pii_entities.length > 0 ? (
                    <span className="bg-red-100 text-red-800 text-xs px-2 py-1 rounded-full font-bold">
                      {doc.pii_entities.length} Found
                    </span>
                  ) : (
                    <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                      Clean
                    </span>
                  )}
                </td>
                <td className="p-3 text-gray-500 truncate max-w-xs" title={doc.full_text}>
                  {doc.full_text.substring(0, 50)}...
                </td>
              </tr>
            ))}
            {documents.length === 0 && (
              <tr>
                <td colSpan={6} className="p-8 text-center text-gray-500">
                  No logs found. Try scanning some text above!
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
