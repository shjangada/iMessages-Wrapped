import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function MainPage() {
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (username.trim()) {
      // Pass the username as state to the ChatPage
      navigate('/chat', { state: { username } });
    } else {
      alert('Please enter a username');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to iMessage Analytics</h1>
      <input
        type="text"
        placeholder="Enter your username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <button onClick={handleSubmit}>Start Chat</button>
    </div>
  );
}

export default MainPage;
