/**
 * API service for communicating with the EngiCalc backend
 */

import axios from 'axios'
import type {
  Document,
  DocumentListItem,
  DocumentMetadata,
  CalculationRequest,
  CalculationResponse,
  Template,
  ExportRequest,
} from '../types'

const API_BASE = '/api'

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Document API
export const documentApi = {
  list: async (): Promise<DocumentListItem[]> => {
    const response = await api.get('/document/list')
    return response.data.documents
  },

  get: async (filename: string): Promise<Document> => {
    const response = await api.get(`/document/${filename}`)
    return response.data
  },

  create: async (
    filename: string,
    metadata: DocumentMetadata = {},
    content: string = ''
  ): Promise<Document> => {
    const response = await api.post('/document/create', {
      filename,
      metadata,
      content,
    })
    return response.data
  },

  update: async (
    filename: string,
    metadata?: DocumentMetadata,
    content?: string
  ): Promise<Document> => {
    const response = await api.put(`/document/${filename}`, {
      metadata,
      content,
    })
    return response.data
  },

  delete: async (filename: string): Promise<void> => {
    await api.delete(`/document/${filename}`)
  },
}

// Calculation API
export const calculationApi = {
  execute: async (request: CalculationRequest): Promise<CalculationResponse> => {
    const response = await api.post('/calculation/execute', request)
    return response.data
  },

  validate: async (code: string): Promise<{ valid: boolean; error?: string }> => {
    const response = await api.post('/calculation/validate', { code })
    return response.data
  },
}

// Template API
export const templateApi = {
  list: async (): Promise<Template[]> => {
    const response = await api.get('/template/list')
    return response.data.templates
  },

  get: async (filename: string): Promise<Template> => {
    const response = await api.get(`/template/${filename}`)
    return response.data
  },

  render: async (
    template_filename: string,
    variables: Record<string, string>
  ): Promise<string> => {
    const response = await api.post('/template/render', {
      template_filename,
      variables,
    })
    return response.data.content
  },
}

// Export API
export const exportApi = {
  pdf: async (request: ExportRequest): Promise<Blob> => {
    const response = await api.post('/export/pdf', request, {
      responseType: 'blob',
    })
    return response.data
  },

  html: async (request: ExportRequest): Promise<Blob> => {
    const response = await api.post('/export/html', request, {
      responseType: 'blob',
    })
    return response.data
  },

  checkPandoc: async (): Promise<{ available: boolean; message: string }> => {
    const response = await api.get('/export/check-pandoc')
    return response.data
  },
}

export default api
