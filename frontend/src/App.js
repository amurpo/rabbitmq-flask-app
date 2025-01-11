import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [receivedMessage, setReceivedMessage] = useState('');
  const [lastMessage, setLastMessage] = useState('');

  const sendMessage = async () => {
    await axios.post('http://localhost:5000/send', { message });
    setMessage('');
  };

  const receiveMessage = async () => {
    const response = await axios.get('http://localhost:5000/receive');
    setReceivedMessage(response.data.message);
  };

  const getLastMessage = async () => {
    const response = await axios.get('http://localhost:5000/last');
    setLastMessage(response.data.message);
  };

  useEffect(() => {
    getLastMessage();
  }, []);

  return (
    <div>
      <h1>RabbitMQ with Flask and React</h1>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send Message</button>
      <button onClick={receiveMessage}>Receive Message</button>
      <h2>Received Message: {receivedMessage}</h2>
      <h2>Last Cached Message: {lastMessage}</h2>
    </div>
  );
}

export default App;
