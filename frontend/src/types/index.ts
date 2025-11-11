/**
 * TypeScript type definitions for EngiCalc
 */

export interface DocumentMetadata {
  project?: string
  engineer?: string
  date?: string
  revision?: string
  title?: string
  description?: string
  [key: string]: any
}

export interface Document {
  filename: string
  metadata: DocumentMetadata
  content: string
  raw_content: string
}

export interface DocumentListItem {
  filename: string
  metadata: DocumentMetadata
  modified: number
  size: number
}

export interface CalculationBlock {
  id?: string
  code: string
  language?: string
}

export interface CalculationResult {
  success: boolean
  latex?: string
  result?: Record<string, any>
  output?: string
  error?: string
  execution_time: number
}

export interface CalculationRequest {
  blocks: CalculationBlock[]
  context?: Record<string, any>
}

export interface CalculationResponse {
  results: CalculationResult[]
  final_context: Record<string, any>
}

export interface Template {
  filename: string
  metadata: {
    name: string
    description?: string
    category?: string
    variables: string[]
  }
  content: string
}

export interface ExportRequest {
  markdown_content: string
  output_filename: string
  metadata?: Record<string, any>
}
