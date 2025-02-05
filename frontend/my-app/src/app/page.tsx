"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [jobDescription, setJobDescription] = useState('');
  const [success, setSuccess] = useState('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles && acceptedFiles[0].type === 'application/pdf') {
      setFile(acceptedFiles[0]);
      setError('');
    } else {
      setError('File must be in PDF format');
      setFile(null);
    }
  }, []);

  const generateDocument = async (type: 'cv' | 'cover-letter') => {
    if (!file || !jobDescription.trim()) {
      setError('Please upload a CV and provide a job description');
      return;
    }
  
    setLoading(true);
    setError('');
    setSuccess('');
  
    try {
      const formData = new FormData();
      formData.append('cv', file);
      formData.append('job_description', jobDescription);

      const response = await fetch(`/api/${type === 'cv' ? 'generate-cv' : 'generate-cover-letter'}`, {
        method: 'POST',
        body: formData,
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Failed to generate ${type === 'cv' ? 'CV' : 'Cover Letter'}`);
      }
  
       // Create a Blob from the response
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      // Create a link element to download the file
      const a = document.createElement('a');
      a.href = url;
      a.download = `${type === 'cv' ? 'generatedCV' : 'generatedCoverLetter'}.tex`; 
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      window.URL.revokeObjectURL(url);

      setSuccess("File downloaded successfully");
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1
  });

  const isGenerateDisabled = !file || !jobDescription.trim() || loading;

  return (
    <div className="w-full bg-gray-100 p-4 flex justify-center items-center my-auto">
      <div className="w-full max-w-4xl min-h-[600px] bg-white flex flex-col items-center rounded-2xl shadow-md">
        <h1 className="w-full text-center text-4xl mt-8 font-bold text-gray-600">CV Crafter</h1>

        <div
          {...getRootProps()}
          className={`py-5 w-5/6 mx-auto text-center rounded-xl cursor-pointer mt-8 mb-5 border-2 border-dashed 
            transition-colors duration-200 ${
              isDragActive ? 'border-blue-600 bg-blue-50' : 'border-blue-400'
            } ${isGenerateDisabled ? 'opacity-50' : ''}`}
        >
          <input {...getInputProps()} />
          <h2 className="text-xl font-bold capitalize mb-2">Upload your CV</h2>
          {isDragActive ? (
            <p className="mb-2 text-gray-400">Drop the files here ...</p>
          ) : (
            <p className="mb-2 text-gray-400">
              Drag and drop some files here, or click to select files
            </p>
          )}
          {file && <p className="mb-2 text-gray-800 font-semibold">{file.name}</p>}
        </div>

        <div className="w-full py-8 flex flex-col items-center">
          <div className="w-5/6">
            <p className="block mb-2 text-xl font-bold text-gray-900">
              Job Description
            </p>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="block p-4 w-full text-sm min-h-[200px] resize-y text-gray-900 bg-gray-50 rounded-lg 
                border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Paste the job description here..."
            />
          </div>
        </div>

        {error && (
          <div className="w-5/6 mb-4 p-4 text-red-600 bg-red-50 rounded-lg text-center">
            {error}
          </div>
        )}

        {success && (
          <div className="w-5/6 mb-4 p-4 text-green-600 bg-green-50 rounded-lg text-center">
            {success}
          </div>
        )}

        <div className="w-5/6 flex flex-col sm:flex-row justify-center gap-4 mb-8">
          <button
            className="px-6 py-3 text-white bg-blue-500 rounded-xl hover:bg-blue-700 
              transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => generateDocument('cv')}
            disabled={isGenerateDisabled}
          >
            {loading ? 'Generating...' : 'Generate Custom CV'}
          </button>
          <button
            className="px-6 py-3 text-white bg-green-500 rounded-xl hover:bg-green-700 
              transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => generateDocument('cover-letter')}
            disabled={isGenerateDisabled}
          >
            {loading ? 'Generating...' : 'Generate Cover Letter'}
          </button>
        </div>
      </div>
    </div>
  );
}