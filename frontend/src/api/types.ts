import type {
    CorrectionEmailDraft, Document, ReviewData 
} from '@/lib/types'

export interface IDocumentApi {
    listDocuments(): Promise<Document[]>
    getDocument(id: string): Promise<Document>
    uploadDocument(file: File): Promise<Document>
    deleteDocument(id: string): Promise<void>
    updateDocument(id: string, data: Omit<ReviewData, 'field_confidence' | 'field_sources'>): Promise<Document>
    decideDocument(id: string, decision: 'approved' | 'rejected'): Promise<Document>
    generateCorrectionEmail(id: string): Promise<CorrectionEmailDraft>
    documentFileUrl(id: string): string
}