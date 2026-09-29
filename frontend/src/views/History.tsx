import { DocumentInbox } from '../components/DocumentInbox'
import { Card } from '../components/ui/card'

import type { Document } from '@/lib/types'

interface HistoryProps {
    documents: Document[]
    historyLoading: boolean
    error: string | null
    onDelete: (document: Document) => Promise<void>
    onSelect: (document: Document) => void
}

export function History({
    documents, error, historyLoading, onDelete, onSelect 
}: Readonly<HistoryProps>) {
    return (
        <main className="mx-auto max-w-4xl px-6 py-10">
            <div className="flex items-end justify-between gap-4">
                <div>
                    <p className="text-sm text-zinc-500">Saved locally</p>
                    <h1 className="mt-1 text-2xl font-semibold tracking-tight">Review history</h1>
                    <p className="mt-1 text-sm text-zinc-600">
                        Open a previous document, or start another review.
                    </p>
                </div>
            </div>
            {error && (
                <div
                    role="alert"
                    className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800"
                >
                    {error}
                </div>
            )}
            <Card className="mt-6 overflow-hidden">
                {historyLoading ? (
                    <p className="p-12 text-center text-sm text-zinc-500">Loading review history…</p>
                ) : (
                    <DocumentInbox
                        documents={documents}
                        onSelect={onSelect}
                        onDelete={onDelete}
                    />
                )}
            </Card>
        </main>
    )
}