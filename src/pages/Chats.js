import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios'; // Ensure axios is imported

function ChatPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { username } = location.state || { username: 'Guest' };

  const [chats, setChats] = useState([]);

  // Fetch chats from the backend
  useEffect(() => {
    axios
      .get('http://127.0.0.1:5000/api/chats')
      .then((response) => {
        // Directly use the data from axios response
        setChats(response.data);
      })
      .catch((error) => {
        console.error('Error fetching chats:', error);
      });
  }, []);

  const handleChatClick = (chatId) => {
    navigate('/messages', { state: { chatId } });
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Hello, {username}!</h1>
      <h2>Available Chats:</h2>
      <ul>
        {chats.map((chat) => (
          <li key={chat.id} onClick={() => handleChatClick(chat.id)}>
            {chat.id}: {chat.messages} messages, {chat.positivity} (Blend Rate: {chat.blend_rate.toFixed(2)})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ChatPage;
