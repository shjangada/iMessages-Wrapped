import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const MessagesPage = () => {
  const navigate = useNavigate();

  const [messagesData, setMessagesData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [specificWord, setSpecificWord] = useState('');
  const [wordCount, setWordCount] = useState(null);

  useEffect(() => {
    axios
      .get('http://127.0.0.1:5000/api/messages')
      .then((response) => {
        setMessagesData(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleSpecificWordSubmit = () => {
    if (!specificWord) return;

    axios
      .post('http://localhost:5000/api/word-count', { word: specificWord })
      .then((response) => setWordCount(response.data.count))
      .catch((err) => setError(err.message));
  };

  if (loading) {
    return <h2 className="text-center mt-8">Loading messages...</h2>;
  }

  if (error) {
    return <h2 className="text-center mt-8 text-red-500">Error: {error}</h2>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-8">Message Analysis</h1>

      {/* Overview Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Overview</h2>
        <div className="space-y-2">
          <p>Total Messages: {messagesData.totalMessages}</p>
          <p>Messages Sent: {messagesData.sentMessages}</p>
          <p>Sent Percentage: {messagesData.sentPercentage.toFixed(2)}%</p>
          <p>Average Message Length: {messagesData.averageLength} words</p>
          <p>Curse Word Count: {messagesData.curseCount}</p>
        </div>
      </div>

      {/* Most Used Words Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Most Used Words</h2>
        <div className="space-y-2">
          {messagesData.frequencyDistribution.map(([word, count], index) => (
            <div key={index} className="flex justify-between border-b py-2">
              <span>{word}</span>
              <span>{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Time Segments Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Messages by Time of Day</h2>
        <div className="space-y-2">
          {Object.entries(messagesData.timeSegments).map(([time, count], index) => (
            <div key={index} className="flex justify-between border-b py-2">
              <span>{time}</span>
              <span>{count}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Word Search Section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Word Search</h2>
        <div className="flex gap-4 mb-4">
          <input
            type="text"
            value={specificWord}
            onChange={(e) => setSpecificWord(e.target.value)}
            placeholder="Enter a word"
            className="flex-1 p-2 border rounded"
          />
          <button
            onClick={handleSpecificWordSubmit}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Search
          </button>
        </div>
        {wordCount !== null && (
          <p>"{specificWord}" appears {wordCount} times in your messages</p>
        )}
      </div>

      <button
        onClick={() => navigate('/chats')}
        className="w-full p-3 bg-gray-100 rounded-lg hover:bg-gray-200"
      >
        Back to Chats
      </button>
    </div>
  );
};

export default MessagesPage;
