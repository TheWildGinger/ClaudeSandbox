/**
 * Zustand store for document state management
 */

import { create } from 'zustand'
import type { Document, DocumentMetadata } from '../types'

interface DocumentState {
  currentDocument: Document | null
  isModified: boolean
  isSaving: boolean
  error: string | null

  // Actions
  setCurrentDocument: (doc: Document | null) => void
  updateContent: (content: string) => void
  updateMetadata: (metadata: DocumentMetadata) => void
  setModified: (modified: boolean) => void
  setSaving: (saving: boolean) => void
  setError: (error: string | null) => void
  reset: () => void
}

export const useDocumentStore = create<DocumentState>((set) => ({
  currentDocument: null,
  isModified: false,
  isSaving: false,
  error: null,

  setCurrentDocument: (doc) => set({ currentDocument: doc, isModified: false }),

  updateContent: (content) =>
    set((state) => ({
      currentDocument: state.currentDocument
        ? { ...state.currentDocument, content }
        : null,
      isModified: true,
    })),

  updateMetadata: (metadata) =>
    set((state) => ({
      currentDocument: state.currentDocument
        ? { ...state.currentDocument, metadata }
        : null,
      isModified: true,
    })),

  setModified: (modified) => set({ isModified: modified }),

  setSaving: (saving) => set({ isSaving: saving }),

  setError: (error) => set({ error }),

  reset: () =>
    set({
      currentDocument: null,
      isModified: false,
      isSaving: false,
      error: null,
    }),
}))
