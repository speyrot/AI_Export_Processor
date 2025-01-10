"use client"

import { useState } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const { signIn } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await signIn(email, password)
      router.push('/')
    } catch (err) {
      setError('Invalid login credentials')
    }
  }

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-light py-5">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-12 col-md-8 col-lg-6 col-xl-5">
            <div className="card shadow-sm border-0">
              <div className="card-body p-4 p-lg-5">
                <div className="text-center mb-4">
                  <i className="bi bi-file-earmark-excel fs-1 text-primary mb-2"></i>
                  <h2 className="fw-bold mb-0">Invoice Processor</h2>
                  <p className="text-muted">Sign in to your account</p>
                </div>

                <form className="mt-4" onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                      Email address
                    </label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="bi bi-envelope"></i>
                      </span>
                      <input
                        id="email"
                        name="email"
                        type="email"
                        required
                        className="form-control"
                        placeholder="name@company.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </div>
                  </div>

                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Password
                    </label>
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="bi bi-lock"></i>
                      </span>
                      <input
                        id="password"
                        name="password"
                        type="password"
                        required
                        className="form-control"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="alert alert-danger d-flex align-items-center" role="alert">
                      <i className="bi bi-exclamation-triangle-fill me-2"></i>
                      {error}
                    </div>
                  )}

                  <div className="d-grid mt-4">
                    <button
                      type="submit"
                      className="btn btn-primary btn-lg"
                    >
                      Sign in
                    </button>
                  </div>
                </form>

                <div className="mt-4 text-center">
                  <Link 
                    href="/signup"
                    className="text-decoration-none"
                  >
                    Need an account? <span className="text-primary">Sign up</span>
                  </Link>
                </div>
              </div>
            </div>

            <div className="text-center mt-4">
              <small className="text-muted">
                © {new Date().getFullYear()} Invoice Processor. All rights reserved.
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 