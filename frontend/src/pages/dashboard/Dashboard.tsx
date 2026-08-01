import { type FC, type ChangeEvent, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { uploadDocument, listDocuments, queryDocuments } from '../../services/documentService';

interface DocumentType {
  id: number;
  filename: string;
  uploaded_at: string;
}

export const Dashboard: FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [documents, setDocuments] = useState<DocumentType[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [question, setQuestion] = useState<string>('');
  const [answer, setAnswer] = useState<string | null>(null);
  const [asking, setAsking] = useState<boolean>(false);

  const fetchDocuments = async () => {
    try {
      const data = await listDocuments();
      setDocuments(data);
    } catch (err) {
      console.error('Failed to fetch documents', err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setError(null);
    try {
      await uploadDocument(selectedFile);
      setSelectedFile(null);
      fetchDocuments();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setAsking(true);
    setAnswer(null);
    try {
      const res = await queryDocuments(question);
      setAnswer(res.answer);
    } catch (err: any) {
      console.error('Failed to query', err);
      setAnswer(err.response?.data?.detail || 'Failed to get an answer.');
    } finally {
      setAsking(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl h-[calc(100vh-2rem)] bg-white p-8 rounded-xl shadow-lg border border-gray-100 flex flex-col">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">
            Welcome, {user?.fullname}
          </h1>
          <p className="text-gray-600">
            {user?.email}
          </p>
        </div>

        <div className="flex-1 overflow-y-auto scrollbar-hide space-y-6">
          {/* Upload & List Section */}
          <div className="text-left bg-gray-50 p-4 rounded-md border border-gray-200">
            <h2 className="text-lg font-semibold mb-4 text-gray-800">Your Documents</h2>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-4">
              <input 
                type="file" 
                onChange={handleFileChange} 
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-md file:border-0
                  file:text-sm file:font-semibold
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
              />
              <button
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                className={`px-4 py-2 font-medium rounded-md text-white transition-colors whitespace-nowrap ${
                  !selectedFile || uploading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                {uploading ? 'Uploading...' : 'Upload'}
              </button>
            </div>
            
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            <div className="max-h-32 overflow-y-auto scrollbar-hide">
              <ul className="divide-y divide-gray-200 border-t border-gray-200">
                {documents.length === 0 ? (
                  <li className="py-4 text-gray-500 text-sm">No documents found.</li>
                ) : (
                  documents.map((doc) => (
                    <li key={doc.id} className="py-3 flex justify-between items-center text-sm">
                      <span className="font-medium text-gray-700">{doc.filename}</span>
                      <span className="text-gray-500">{new Date(doc.uploaded_at).toLocaleDateString()}</span>
                    </li>
                  ))
                )}
              </ul>
            </div>
          </div>
          
          {/* Chat Section */}
          <div className="text-left bg-gray-50 p-4 rounded-md border border-gray-200">
            <h2 className="text-lg font-semibold mb-4 text-gray-800">Ask your Documents</h2>
            
            <div className="flex flex-col sm:flex-row gap-4 mb-4">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !asking && question.trim() && handleAsk()}
                placeholder="Ask a question..."
                className="flex-1 px-4 py-2 text-sm text-gray-900 bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <button
                onClick={handleAsk}
                disabled={!question.trim() || asking}
                className={`px-4 py-2 font-medium rounded-md text-white transition-colors whitespace-nowrap ${
                  !question.trim() || asking ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                {asking ? 'Asking...' : 'Ask'}
              </button>
            </div>
            
            {answer && (
              <div className="mt-4 p-4 bg-white border border-gray-200 rounded-md h-64 overflow-y-auto scrollbar-hide">
                <p className="text-sm text-gray-800 whitespace-pre-wrap">{answer}</p>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 text-center">
          <button
            onClick={handleLogout}
            className="w-full sm:w-auto px-6 py-2 bg-red-600 text-white font-medium rounded-md hover:bg-red-700 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};
