// frontend/src/components/UploadForm/index.tsx

"use client"

import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { supabase } from '@/lib/supabase'
import { useAuth } from '@/contexts/AuthContext'
import { ProcessedFiles } from '@/components/ProcessedFiles'

// Add type for the signed URL response
type SignedUrlResponse = {
  data: {
    signedUrl: string
  } | null
  error: Error | null
}

export function UploadForm() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [processedFileUrl, setProcessedFileUrl] = useState<string | null>(null)
  const { user } = useAuth()

  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    
    // Validate file type
    if (!file.name.endsWith('.xls') && !file.name.endsWith('.xlsx')) {
      setError('Please upload an Excel file (.xls or .xlsx)')
      return
    }

    try {
      setError(null)
      setIsProcessing(true)

      // Upload to Supabase Storage
      const timestamp = new Date().getTime()
      const randomId = Math.random().toString(36).substring(2, 15)
      const filePath = `uploads/${user?.id}/${timestamp}_${randomId}_${file.name}`
      
      console.log('Attempting upload:', {
        bucket: 'invoices',
        filePath,
        fileSize: file.size,
        fileType: file.type
      })

      const { error: uploadError, data: uploadData } = await supabase.storage
        .from('invoices')
        .upload(filePath, file)

      if (uploadError) {
        console.error('Supabase upload error:', uploadError)
        throw uploadError
      }

      // Get signed URL that's valid for 1 hour
      const { data, error: signUrlError }: SignedUrlResponse = await supabase.storage
        .from('invoices')
        .createSignedUrl(filePath, 3600)

      if (signUrlError || !data?.signedUrl) {
        throw new Error('Failed to get signed URL')
      }

      console.log('Upload successful, signed URL:', data.signedUrl)

      // Send to backend for processing
      const response = await fetch('http://localhost:8000/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          fileUrl: data.signedUrl,
          userId: user?.id,
          originalFileName: file.name
        }),
      })

      const responseData = await response.json()

      if (!response.ok) {
        console.error('Backend processing error:', responseData)
        throw new Error(responseData.detail || 'Processing failed')
      }

      console.log('Processing result:', responseData)
      
      // Set the processed file URL
      setProcessedFileUrl(responseData.fileUrl)
      setIsProcessing(false)
      
    } catch (err: any) {
      const errorMessage = err.message || 'Error processing file. Please try again.'
      setError(errorMessage)
      console.error('Upload/Processing error:', {
        message: err.message,
        error: err,
        stack: err.stack,
        name: err.name,
        code: err.code
      })
      setIsProcessing(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    maxFiles: 1
  })

  return (
    <div>
      <div
        {...getRootProps()}
        className={`
          border-2 rounded-3 p-5 text-center cursor-pointer
          d-flex flex-column align-items-center justify-content-center
          ${isDragActive 
            ? 'bg-primary bg-opacity-10 border-primary' 
            : 'bg-light border-dashed'
          }
        `}
        style={{ minHeight: '200px' }}
      >
        <input {...getInputProps()} />
        <i className="bi bi-file-earmark-excel mb-3 fs-1 text-primary"></i>
        {isDragActive ? (
          <p className="mb-0 text-primary">Drop the Excel file here...</p>
        ) : (
          <>
            <p className="mb-2">Drag and drop an Excel file here, or click to select</p>
            <small className="text-muted">Supports .xls and .xlsx files</small>
          </>
        )}
      </div>

      {isProcessing && (
        <div className="alert alert-info mt-4 d-flex align-items-center" role="alert">
          <div className="spinner-border spinner-border-sm me-2" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          Processing your invoice...
        </div>
      )}

      {error && (
        <div className="alert alert-danger mt-4" role="alert">
          {error}
        </div>
      )}

      {processedFileUrl && <ProcessedFiles fileUrl={processedFileUrl} />}
    </div>
  )
} 