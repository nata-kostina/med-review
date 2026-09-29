import { mockDocuments } from './mockData'

import type { IDocumentApi } from './types'
import type { CorrectionEmailDraft } from '@/lib/types'

const delay = (ms = 0) => new Promise((resolve) => setTimeout(resolve, ms))

export const mockDocumentApi: IDocumentApi = {
    async listDocuments() {
        await delay()
        return mockDocuments.slice(1)
    },

    async getDocument(id) {
        await delay()
        const doc = mockDocuments.find((d) => d.id === id)
        if (!doc) throw new Error('Document not found')
        return doc
    },

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    async uploadDocument(_file) {
        await delay(2500)
        return mockDocuments[0]
    },

    async deleteDocument(id) {
        await delay()
        const index = mockDocuments.findIndex((d) => d.id === id)
        if (index !== -1) {
            mockDocuments.splice(index, 1)
        }
    },

    async updateDocument(id, data) {
        await delay()
        const doc = await this.getDocument(id)
        return {
            ...doc,
            ...data 
        }
    },

    async decideDocument(id, decision) {
        await delay(3000)
        const doc = await this.getDocument(id)
        return {
            ...doc,
            status: decision 
        }
    },

    async generateCorrectionEmail(id) {
        await delay()
        return {
            subject: `Correction needed for ${id}`,
            body: 'Please fix the highlighted sections.',
            recipient_name: 'Recipient Name'
        } as CorrectionEmailDraft
    },

    documentFileUrl(id) {
        return `https://via.placeholder.com/150?text=Doc+${id}`
    },
}