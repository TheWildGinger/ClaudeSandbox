import { useState, useEffect } from 'react'
import { documentApi, templateApi } from '../services/api'
import { useDocumentStore } from '../stores/documentStore'
import type { DocumentListItem, Template } from '../types'

export default function Sidebar() {
  const [activeTab, setActiveTab] = useState<'documents' | 'templates'>('documents')
  const [documents, setDocuments] = useState<DocumentListItem[]>([])
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(false)

  const { setCurrentDocument, currentDocument } = useDocumentStore()

  // Load documents
  useEffect(() => {
    if (activeTab === 'documents') {
      loadDocuments()
    }
  }, [activeTab])

  // Load templates
  useEffect(() => {
    if (activeTab === 'templates') {
      loadTemplates()
    }
  }, [activeTab])

  const loadDocuments = async () => {
    setLoading(true)
    try {
      const docs = await documentApi.list()
      setDocuments(docs)
    } catch (error) {
      console.error('Failed to load documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadTemplates = async () => {
    setLoading(true)
    try {
      const temps = await templateApi.list()
      setTemplates(temps)
    } catch (error) {
      console.error('Failed to load templates:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDocumentClick = async (filename: string) => {
    try {
      const doc = await documentApi.get(filename)
      setCurrentDocument(doc)
    } catch (error) {
      console.error('Failed to load document:', error)
    }
  }

  const handleTemplateClick = async (template: Template) => {
    try {
      // For MVP, just insert template content
      // In future, could prompt for variables
      const content = template.content
      const newDoc = await documentApi.create(
        `new-from-template-${Date.now()}.md`,
        {
          title: template.metadata.name,
          description: template.metadata.description,
        },
        content
      )
      setCurrentDocument(newDoc)
      setActiveTab('documents')
      loadDocuments()
    } catch (error) {
      console.error('Failed to create document from template:', error)
    }
  }

  const handleNewDocument = async () => {
    try {
      const newDoc = await documentApi.create(`new-document-${Date.now()}.md`, {
        title: 'New Document',
        date: new Date().toISOString().split('T')[0],
      })
      setCurrentDocument(newDoc)
      loadDocuments()
    } catch (error) {
      console.error('Failed to create document:', error)
    }
  }

  return (
    <div className="w-64 bg-gray-100 border-r border-gray-200 flex flex-col">
      {/* Tabs */}
      <div className="flex border-b border-gray-300">
        <button
          className={`flex-1 py-2 px-4 text-sm font-medium ${
            activeTab === 'documents'
              ? 'bg-white border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
          onClick={() => setActiveTab('documents')}
        >
          Documents
        </button>
        <button
          className={`flex-1 py-2 px-4 text-sm font-medium ${
            activeTab === 'templates'
              ? 'bg-white border-b-2 border-blue-500 text-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
          onClick={() => setActiveTab('templates')}
        >
          Templates
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === 'documents' && (
          <div className="p-2">
            <button
              onClick={handleNewDocument}
              className="w-full mb-2 px-3 py-2 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
            >
              + New Document
            </button>

            {loading ? (
              <div className="text-center text-gray-500 text-sm mt-4">Loading...</div>
            ) : (
              <div className="space-y-1">
                {documents.map((doc) => (
                  <button
                    key={doc.filename}
                    onClick={() => handleDocumentClick(doc.filename)}
                    className={`w-full text-left px-3 py-2 rounded text-sm hover:bg-gray-200 ${
                      currentDocument?.filename === doc.filename
                        ? 'bg-blue-100 border-l-2 border-blue-600'
                        : 'bg-white'
                    }`}
                  >
                    <div className="font-medium truncate">{doc.filename}</div>
                    {doc.metadata.project && (
                      <div className="text-xs text-gray-600 truncate">
                        {doc.metadata.project}
                      </div>
                    )}
                  </button>
                ))}
                {documents.length === 0 && (
                  <div className="text-center text-gray-500 text-sm mt-4">
                    No documents yet
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {activeTab === 'templates' && (
          <div className="p-2">
            {loading ? (
              <div className="text-center text-gray-500 text-sm mt-4">Loading...</div>
            ) : (
              <div className="space-y-1">
                {templates.map((template) => (
                  <button
                    key={template.filename}
                    onClick={() => handleTemplateClick(template)}
                    className="w-full text-left px-3 py-2 rounded text-sm bg-white hover:bg-gray-200"
                  >
                    <div className="font-medium">{template.metadata.name}</div>
                    {template.metadata.description && (
                      <div className="text-xs text-gray-600 mt-1">
                        {template.metadata.description}
                      </div>
                    )}
                  </button>
                ))}
                {templates.length === 0 && (
                  <div className="text-center text-gray-500 text-sm mt-4">
                    No templates available
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
