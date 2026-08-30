import * as React from "react"
import { X } from "lucide-react"

const Dialog = ({ children, open, onOpenChange }) => {
  React.useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && open) {
        onOpenChange(false)
      }
    }
    
    if (open) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [open, onOpenChange])

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div 
        className="fixed inset-0 bg-black bg-opacity-50"
        onClick={() => onOpenChange(false)}
      />
      {children}
    </div>
  )
}

const DialogContent = ({ children, className = "", ...props }) => {
  return (
    <div 
      className={`relative bg-white rounded-lg shadow-lg p-6 w-full max-w-lg mx-4 ${className}`}
      onClick={(e) => e.stopPropagation()}
      {...props}
    >
      {children}
    </div>
  )
}

const DialogHeader = ({ children, className = "", ...props }) => {
  return (
    <div className={`mb-4 ${className}`} {...props}>
      {children}
    </div>
  )
}

const DialogTitle = ({ children, className = "", ...props }) => {
  return (
    <h2 className={`text-xl font-semibold ${className}`} {...props}>
      {children}
    </h2>
  )
}

const DialogDescription = ({ children, className = "", ...props }) => {
  return (
    <p className={`text-gray-600 mt-2 ${className}`} {...props}>
      {children}
    </p>
  )
}

export { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription }

