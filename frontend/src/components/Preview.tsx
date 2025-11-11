import { useEffect, useState, useCallback } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import remarkGfm from 'remark-gfm'
import rehypeKatex from 'rehype-katex'
import { useDocumentStore } from '../stores/documentStore'
import { calculationApi } from '../services/api'
import type { CalculationResult } from '../types'

// Custom code block renderer for Python calculations
function CodeBlock({ node, inline, className, children, ...props }: any) {
  const [result, setResult] = useState<CalculationResult | null>(null)
  const [isExecuting, setIsExecuting] = useState(false)

  const code = String(children).replace(/\n$/, '')
  const match = /language-(\w+)/.exec(className || '')
  const language = match ? match[1] : ''

  const executeCalculation = useCallback(async () => {
    // Check if this is a calculation block
    if (language === 'python' && code.includes('%%calc')) {
      setIsExecuting(true)
      try {
        // Remove %%calc marker
        const cleanCode = code.replace(/%%calc\s*\n?/, '')

        const response = await calculationApi.execute({
          blocks: [{ code: cleanCode, language: 'python' }],
          context: {},
        })

        if (response.results.length > 0) {
          setResult(response.results[0])
        }
      } catch (error) {
        console.error('Calculation error:', error)
        setResult({
          success: false,
          error: 'Failed to execute calculation',
          execution_time: 0,
        })
      } finally {
        setIsExecuting(false)
      }
    }
  }, [code, language])

  useEffect(() => {
    if (language === 'python' && code.includes('%%calc')) {
      executeCalculation()
    }
  }, [code, language, executeCalculation])

  // Regular code block (not a calculation)
  if (!code.includes('%%calc')) {
    return (
      <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
        <code className={className} {...props}>
          {children}
        </code>
      </pre>
    )
  }

  // Calculation block with results
  return (
    <div className="my-4 border border-blue-200 rounded-lg overflow-hidden">
      {/* Code */}
      <div className="bg-gray-50 p-4 border-b border-blue-200">
        <pre className="text-sm">
          <code>{code.replace(/%%calc\s*\n?/, '')}</code>
        </pre>
      </div>

      {/* Results */}
      <div className="bg-white p-4">
        {isExecuting && (
          <div className="text-blue-600 text-sm">Executing...</div>
        )}

        {!isExecuting && result && (
          <>
            {result.success ? (
              <div>
                {/* LaTeX rendering */}
                {result.latex && (
                  <div className="mb-4">
                    <div
                      dangerouslySetInnerHTML={{
                        __html: `$$${result.latex}$$`,
                      }}
                    />
                  </div>
                )}

                {/* Output */}
                {result.output && (
                  <div className="mb-2">
                    <pre className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                      {result.output}
                    </pre>
                  </div>
                )}

                {/* Variables */}
                {result.result && Object.keys(result.result).length > 0 && (
                  <div className="text-sm">
                    <div className="font-semibold mb-1">Variables:</div>
                    <div className="space-y-1">
                      {Object.entries(result.result).map(([key, value]) => (
                        <div key={key} className="flex gap-2">
                          <span className="font-mono text-blue-600">{key}:</span>
                          <span className="font-mono">
                            {typeof value === 'object' && value !== null && 'formatted' in value
                              ? value.formatted
                              : JSON.stringify(value)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="text-xs text-gray-500 mt-2">
                  Execution time: {result.execution_time.toFixed(3)}s
                </div>
              </div>
            ) : (
              <div className="text-red-600 text-sm">
                <div className="font-semibold">Error:</div>
                <pre className="mt-1 bg-red-50 p-2 rounded">{result.error}</pre>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default function Preview() {
  const { currentDocument } = useDocumentStore()

  const content = currentDocument?.content || ''

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-white">
      <article className="prose prose-slate max-w-none">
        <ReactMarkdown
          remarkPlugins={[remarkMath, remarkGfm]}
          rehypePlugins={[rehypeKatex]}
          components={{
            code: CodeBlock,
          }}
        >
          {content}
        </ReactMarkdown>
      </article>
    </div>
  )
}
