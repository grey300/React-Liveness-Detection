import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="container">
      <h1>Face Recognition System</h1>
      <div className="button-group">
        <Link to="/register"><button>Register Face</button></Link>
        <Link to="/detect"><button>Detect Face</button></Link>
      </div>
    </div>
  );
}
