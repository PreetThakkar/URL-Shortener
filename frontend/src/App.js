import './App.css';
import URLStats from './components/URLStats';
import URLShortener from './components/URLShortener';

const App = () => {
  return (
    <div className="app">
      <header className="hero-section">
        <div className="container text-center">
          <h1 className="hero-title">Shorten Your URLs in Seconds</h1>
          <p className="hero-subtitle">Make your links cleaner, shorter, and easier to share!</p>
        </div>
      </header>

      <main className="container mt-5">
        <URLShortener />
        <URLStats />
      </main>
    </div>
  );
};

export default App;
