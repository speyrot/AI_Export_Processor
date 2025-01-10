"use client"

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { UploadForm } from '@/components/UploadForm'
import { ProcessedFiles } from '@/components/ProcessedFiles'

export default function Home() {
  const { user, loading, signOut } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [loading, user, router])

  if (loading || !user) {
    return (
      <div className="min-vh-100 d-flex align-items-center justify-content-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    )
  }

  const handleSignOut = async () => {
    try {
      await signOut()
      router.push('/login')
    } catch (error) {
      console.error('Error signing out:', error)
    }
  }

  return (
    <div className="container py-5">
      <nav className="navbar navbar-light bg-white shadow-sm rounded-3 mb-4 px-4 py-3">
        <div className="container-fluid px-0">
          <span className="navbar-brand mb-0 h1">Invoice Processor</span>
          <button 
            onClick={handleSignOut}
            className="btn btn-outline-secondary btn-sm"
          >
            Sign Out
          </button>
        </div>
      </nav>
      
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow-sm border-0">
            <div className="card-body p-4">
              <h5 className="card-title mb-4">Upload Invoice</h5>
              <UploadForm />
            </div>
          </div>

          <ProcessedFiles />
        </div>
      </div>
    </div>
  )
}
