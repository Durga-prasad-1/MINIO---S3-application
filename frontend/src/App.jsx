import React, { useState, useEffect } from 'react';
import './App.css';
import FileList from './components/FileList';


const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [responseData, setResponseData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [files, setFiles] = useState([]); // 👈 New state for file list

  // 🔄 Fetch files from backend
  const fetchFiles = async () => {
    try {
      const response = await fetch('http://localhost:8000/files');
      const data = await response.json();
      setFiles(data.files || []);
    } catch (error) {
      console.error('Error fetching files:', error);
    }
  };

  useEffect(() => {
    fetchFiles(); // Load files on page load
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus('');
      setResponseData(null);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) return setUploadStatus('Please select a file first!');

    setIsLoading(true);
    setUploadStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error(`Upload failed: ${response.statusText}`);

      const result = await response.json();
      setResponseData(result);
      setUploadStatus('Upload successful!');
      fetchFiles(); // 👈 Refresh file list after upload
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus(`Upload failed: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setUploadStatus('');
    setResponseData(null);
    document.getElementById('file-input').value = '';
  };

  return (
    <div className="file-upload-container">
      <div className="upload-card">
        <h1 className="upload-title">File Upload</h1>
        <p className="upload-subtitle">Select a file to upload to the server</p>

        {/* Upload Form */}
        <form onSubmit={handleSubmit} className="upload-form">
          <div className={`file-input-area ${selectedFile ? 'file-selected' : ''}`}>
            <input
              type="file"
              id="file-input"
              onChange={handleFileChange}
              className="file-input"
              disabled={isLoading}
            />
            <label htmlFor="file-input" className="file-label">
              <div className="upload-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
              {selectedFile ? (
                <div className="file-info">
                  <p className="file-name">{selectedFile.name}</p>
                  <p className="file-size">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              ) : (
                <>
                  <p className="browse-text">Click to browse files</p>
                  <p className="browse-subtext">Supports all file types</p>
                </>
              )}
            </label>
          </div>

          <div className="button-group">
            <button type="submit" className="upload-button" disabled={!selectedFile || isLoading}>
              {isLoading ? (
                <>
                  <div className="spinner"></div>
                  Uploading...
                </>
              ) : (
                'Upload File'
              )}
            </button>

            {selectedFile && !isLoading && (
              <button type="button" className="reset-button" onClick={resetForm}>
                Clear
              </button>
            )}
          </div>
        </form>

        {/* Status Message */}
        {uploadStatus && (
          <div className={`status-message ${uploadStatus.includes('successful') ? 'success' : 'error'}`}>
            {uploadStatus}
          </div>
        )}


      <FileList files={files}/>
      </div>

        
      
    </div>
  );
};

export default FileUpload;
