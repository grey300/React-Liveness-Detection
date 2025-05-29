import { useState } from 'react';
import axios from 'axios';

export default function Register() {
  const [name, setName] = useState('');
  const [started, setStarted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post('http://localhost:5000/register', new URLSearchParams({ name }));
    setStarted(true);
  };

  return (
    <div className="container">
      <h2>Register New Face</h2>
      {!started ? (
        <form onSubmit={handleSubmit}>
          <label>Name:</label>
          <input type="text" value={name} onChange={e => setName(e.target.value)} required />
          <button type="submit">Start Camera</button>
        </form>
      ) : (
        <>
          <img src="http://localhost:5000/video_feed" alt="Video Feed" style={{ borderRadius: '12px' }} />
          <br />
          <button onClick={() => window.location.href = '/'}>Back to Home</button>
        </>
      )}
    </div>
  );
}
