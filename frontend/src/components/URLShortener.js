// components/URLShortener.js
import React, { useState } from "react";
import axios from "axios";
import '@fortawesome/fontawesome-free/css/all.min.css';

function URLShortener() {
  const [url, setUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [loading, setloading] = useState(false);
  const [error, setError] = useState("");
  const [copySuccess, setCopySuccess] = useState('');

  const apiUrl = process.env.REACT_APP_SHORTEN_ENDPOINT;

  const shortenURL = async () => {
    setShortUrl(null)
    setError("");
    setloading(true)
    try {
      const response = await axios.post(
        `${apiUrl}/`, 
        { "url": url },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (response.status === 503) {setError("Too many requests. Please try again after some time.")}
      else { setShortUrl(`${apiUrl}/${response.data.short_url}`) }
    } catch (error) {
      console.error("Error shortening URL:", error);
      setError("Failed to shorten URL.");
    }
    setloading(false)
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shortUrl).then(() => {
      setCopySuccess('Copied to clipboard!');
      setTimeout(() => setCopySuccess(''), 2000);
    });
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-8">
        <div className="card shadow-lg">
          <div className="card-body">
            <h4 className="card-title text-center mb-4">Paste your long URL below</h4>
            <div className="input-group mb-3">
              <input
                type="text"
                className="form-control"
                placeholder="Enter your long URL"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <button
                className="btn btn-primary"
                type="button"
                onClick={shortenURL}
                disabled={loading}
              >
                {loading ? 'Shortening...' : 'Shorten URL'}
              </button>
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            {shortUrl && (
              <div className="card-body">
                <h6>Your shortened URL:</h6>
                <a href={shortUrl} target="_blank" rel="noopener noreferrer" className="btn btn-link"> {shortUrl}</a>
                <button
                  className="btn"
                  onClick={copyToClipboard}
                ><i className="fas fa-copy me-2"></i></button>
                {copySuccess && (
                  <div className="mt-2 text-success">
                    {copySuccess}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default URLShortener;
