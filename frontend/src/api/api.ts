import type { IDocumentApi } from './types'
import type { CorrectionEmailDraft, Document } from '@/lib/types'

import { apiBaseUrl } from '@/lib/env'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(`${apiBaseUrl}${path}`, {...init})

    if (!response.ok) {
        let message = `Request failed (${response.status})`
        try {
            const body = (await response.json()) as { detail?: string }
            if (typeof body.detail === 'string' && body.detail) {
                message = body.detail
            }
        } catch {
            // Keep the HTTP fallback when the server did not return JSON.
        }
        throw new Error(message)
    }
    if (response.status === 204) {
        return undefined as T
    }
    return response.json() as Promise<T>
}

export const realDocumentApi: IDocumentApi = {
    listDocuments: () => request<Document[]>('/api/documents'),
    getDocument: (id) => request<Document>(`/api/documents/${encodeURIComponent(id)}`),
    uploadDocument: (file) => {
        const body = new FormData()
        body.append('file', file)
        return request<Document>('/api/documents', {
            method: 'POST',
            body 
        })
    },
    deleteDocument: (id) => request<void>(`/api/documents/${encodeURIComponent(id)}`, { method: 'DELETE' }),
    updateDocument: (id, data) => request<Document>(`/api/documents/${encodeURIComponent(id)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    }),
    decideDocument: (id, decision) => request<Document>(`/api/documents/${encodeURIComponent(id)}/decision`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decision }),
    }),
    generateCorrectionEmail: (id) => request<CorrectionEmailDraft>(
        `/api/documents/${encodeURIComponent(id)}/correction-email`,
        { method: 'POST' }
    ),
    documentFileUrl: (id) => `${apiBaseUrl}/api/documents/${encodeURIComponent(id)}/file`,
}
