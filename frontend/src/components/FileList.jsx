import React from 'react';
import "./FileList.css"

const FileList = ({files}) => {
  

  return (
    <div className="file-list">
      <h2>📂 Stored Files</h2>
      <div className="file-grid">
        {files.map((file, idx) => (
          <div key={idx} className="file-card">
            {file.name.match(/\.(jpg|jpeg|png|gif)$/i) ? (
              <img src={file.url} alt={file.name} className="file-preview" />
            ) : (
              <a href={file.url} target="_blank" rel="noreferrer">{file.name}</a>
            )}
            <p className="file-source">Source: {file.source}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FileList;
