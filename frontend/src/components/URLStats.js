import React, { useState } from "react";
import axios from "axios";

function URLStats() {
  const [shortUrl, setShortUrl] = useState("");
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const apiUrl = process.env.REACT_APP_SHORTEN_ENDPOINT;

  const fetchStats = async () => {
    setStats(null);
    setError("");
    setLoading(true)
    try {
      const cleanedShortUrl = shortUrl.startsWith(apiUrl)
      ? shortUrl.slice(apiUrl.length + 1)
      : shortUrl;

      const response = await axios.post(
        `${apiUrl}/stats`,
        { "url": cleanedShortUrl },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setStats(response.data.info);
    } catch (err) {
      console.error("Error fetching stats:", err);
      if (err.response.status === 503) {setError("Too many requests. Please try again after some time.")}
      else {setError("Failed to fetch stats. Please check the shortened URL.");}
    }
    setLoading(false)
  };

  return (
    <div className="row justify-content-center mt-5">
      <div className="col-md-8">
        <div className="card shadow-lg">
          <div className="card-body">
            <h4 className="card-title text-center mb-4">Get Details for a Short URL</h4>
            <div className="input-group mb-3">
              <input
                type="text"
                className="form-control"
                placeholder="Enter your short URL"
                value={shortUrl}
                onChange={(e) => setShortUrl(e.target.value)}
              />
              <button
                className="btn btn-primary"
                type="button"
                onClick={fetchStats}
                disabled={loading}
              >
                {loading ? 'Fetching...' : 'Fetch Details'}
              </button>
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            {stats && (
              <div className="details-card mt-4 p-4 rounded">
                <h5 className="text-center mb-4">Details</h5>
                <div className="detail-item">
                  <strong>Original URL:</strong>
                  <p><a className="text-primary" href={stats.url}>{stats.url}</a></p>
                </div>
                <div className="detail-item">
                  <strong>Visit Count:</strong>
                  <p className="text-success">{stats.visits}</p>
                </div>
                <div className="detail-item">
                  <strong>Last Accessed:</strong>
                  <p className="text-secondary">{new Date(stats.last_accessed).toLocaleString()}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default URLStats;
