// frontend/src/components/ProcessedFiles/index.tsx

interface ProcessedFilesProps {
  fileUrl: string
}

export function ProcessedFiles({ fileUrl }: ProcessedFilesProps) {
  if (!fileUrl) return null;

  return (
    <div className="card shadow-sm border-0 mt-4">
      <div className="card-body p-4">
        <h5 className="card-title mb-4">Processed File</h5>
        <div className="alert alert-success d-flex align-items-center" role="alert">
          <i className="bi bi-check-circle-fill me-2"></i>
          Your file has been processed successfully!
        </div>
        <a 
          href={fileUrl}
          className="btn btn-primary"
          target="_blank"
          rel="noopener noreferrer"
        >
          <i className="bi bi-download me-2"></i>
          Download Processed Invoice
        </a>
      </div>
    </div>
  )
} 