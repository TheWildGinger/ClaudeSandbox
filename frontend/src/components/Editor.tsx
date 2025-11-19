import { useRef } from 'react'
import MonacoEditor from '@monaco-editor/react'
import { useDocumentStore } from '../stores/documentStore'

export default function Editor() {
  const { currentDocument, updateContent } = useDocumentStore()
  const editorRef = useRef<any>(null)

  const handleEditorDidMount = (editor: any) => {
    editorRef.current = editor

    // Configure editor options
    editor.updateOptions({
      fontSize: 14,
      wordWrap: 'on',
      minimap: { enabled: false },
      lineNumbers: 'on',
      scrollBeyondLastLine: false,
      renderWhitespace: 'selection',
    })
  }

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      updateContent(value)
    }
  }

  // Default content when no document is open
  const defaultContent = `---
project: "My Project"
engineer: "Your Name"
date: "2025-11-11"
revision: "A"
---

# Engineering Calculation

## Introduction

This is an example engineering calculation document.

## Calculations

\`\`\`python
%%calc
# Define basic parameters
L = 5.0 * ureg.meter
w = 10.0 * ureg.kN / ureg.meter

# Calculate maximum moment
M_max = w * L**2 / 8

print(f"Maximum moment: {M_max:.2f}")
\`\`\`

## Results

The maximum moment in the beam is calculated above.

![Free Body Diagram](./images/fbd.png)
`

  const editorValue = currentDocument?.content || defaultContent

  return (
    <div className="flex-1 overflow-hidden">
      <MonacoEditor
        height="100%"
        defaultLanguage="markdown"
        value={editorValue}
        onChange={handleEditorChange}
        onMount={handleEditorDidMount}
        theme="vs-light"
        options={{
          automaticLayout: true,
        }}
      />
    </div>
  )
}
