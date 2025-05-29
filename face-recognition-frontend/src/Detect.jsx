export default function Detect() {
  return (
    <div className="container">
      <h2>Detect Face</h2>
      <img src="http://localhost:5000/detect" style={{ display: 'none' }} alt="trigger" />
      <img src="http://localhost:5000/video_feed" alt="Live video" style={{ borderRadius: '12px' }} />
      <br />
      <button onClick={() => window.location.href = '/'}>Back to Home</button>
    </div>
  );
}
