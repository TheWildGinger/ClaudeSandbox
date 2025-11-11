import { useState } from 'react'
import Editor from './components/Editor'
import Preview from './components/Preview'
import Sidebar from './components/Sidebar'
import Toolbar from './components/Toolbar'
import { useDocumentStore } from './stores/documentStore'

function App() {
  const [showSidebar, setShowSidebar] = useState(true)
  const { currentDocument } = useDocumentStore()

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Toolbar */}
      <Toolbar onToggleSidebar={() => setShowSidebar(!showSidebar)} />

      {/* Main content area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar */}
        {showSidebar && <Sidebar />}

        {/* Editor pane */}
        <div className="flex-1 flex flex-col border-r border-gray-200 bg-white">
          <div className="p-2 border-b border-gray-200 bg-gray-50">
            <h2 className="text-sm font-semibold text-gray-700">
              {currentDocument?.filename || 'No document open'}
            </h2>
          </div>
          <Editor />
        </div>

        {/* Preview pane */}
        <div className="flex-1 flex flex-col bg-white">
          <div className="p-2 border-b border-gray-200 bg-gray-50">
            <h2 className="text-sm font-semibold text-gray-700">Preview</h2>
          </div>
          <Preview />
        </div>
      </div>

      {/* Status bar */}
      <div className="h-6 bg-gray-800 text-gray-200 text-xs flex items-center px-4">
        <span>EngiCalc v0.1.0</span>
        {currentDocument && (
          <span className="ml-4">
            {currentDocument.metadata.project && `Project: ${currentDocument.metadata.project}`}
          </span>
        )}
      </div>
    </div>
  )
}

export default App
