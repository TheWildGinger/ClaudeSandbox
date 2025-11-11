import { useState } from 'react'
import { useDocumentStore } from '../stores/documentStore'
import { documentApi, exportApi } from '../services/api'

interface ToolbarProps {
  onToggleSidebar: () => void
}

export default function Toolbar({ onToggleSidebar }: ToolbarProps) {
  const { currentDocument, isModified, setSaving, updateContent, updateMetadata } =
    useDocumentStore()
  const [exporting, setExporting] = useState(false)

  const handleSave = async () => {
    if (!currentDocument) return

    setSaving(true)
    try {
      await documentApi.update(
        currentDocument.filename,
        currentDocument.metadata,
        currentDocument.content
      )
      alert('Document saved successfully!')
    } catch (error) {
      console.error('Save error:', error)
      alert('Failed to save document')
    } finally {
      setSaving(false)
    }
  }

  const handleExportPDF = async () => {
    if (!currentDocument) {
      alert('No document open')
      return
    }

    setExporting(true)
    try {
      // Check if Pandoc is available
      const pandocStatus = await exportApi.checkPandoc()
      if (!pandocStatus.available) {
        alert(pandocStatus.message)
        return
      }

      const blob = await exportApi.pdf({
        markdown_content: currentDocument.raw_content || currentDocument.content,
        output_filename: currentDocument.filename.replace('.md', '.pdf'),
        metadata: currentDocument.metadata,
      })

      // Download the file
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = currentDocument.filename.replace('.md', '.pdf')
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      alert('PDF exported successfully!')
    } catch (error) {
      console.error('Export error:', error)
      alert('Failed to export PDF. Make sure Pandoc is installed.')
    } finally {
      setExporting(false)
    }
  }

  return (
    <div className="h-12 bg-white border-b border-gray-200 flex items-center px-4 gap-2">
      {/* Logo/Title */}
      <div className="flex items-center gap-2">
        <button
          onClick={onToggleSidebar}
          className="p-1 hover:bg-gray-100 rounded"
          title="Toggle sidebar"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
        <h1 className="text-lg font-bold text-gray-800">EngiCalc</h1>
      </div>

      {/* Spacer */}
      <div className="flex-1" />

      {/* Actions */}
      <div className="flex items-center gap-2">
        {isModified && (
          <span className="text-xs text-orange-600 font-medium">Unsaved changes</span>
        )}

        <button
          onClick={handleSave}
          disabled={!currentDocument || !isModified}
          className="px-4 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Save
        </button>

        <button
          onClick={handleExportPDF}
          disabled={!currentDocument || exporting}
          className="px-4 py-1.5 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {exporting ? 'Exporting...' : 'Export PDF'}
        </button>
      </div>
    </div>
  )
}
