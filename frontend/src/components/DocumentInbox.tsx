import { useState } from 'react'

import { StatusBadge } from './StatusBadge'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle
} from './ui/alert-dialog'

import type { Document } from '@/lib/types'

interface DocumentInboxProps {
    documents: Document[]
    onDelete: (document: Document) => Promise<void>
    onSelect: (document: Document) => void
}

function displayName(document: Document): string {
    return document.review_data?.patient_name ?? document.original_filename
}

export function DocumentInbox({
    documents, onDelete, onSelect
}: Readonly<DocumentInboxProps>) {
    const [pendingDelete, setPendingDelete] = useState<Document | null>(null)
    const [deleting, setDeleting] = useState(false)

    async function remove() {
        if (!pendingDelete) return
        setDeleting(true)
        try {
            await onDelete(pendingDelete)
        } catch {
            // Parent keeps the API error visible above the history list.
        } finally {
            setDeleting(false)
            setPendingDelete(null)
        }
    }

    if (documents.length === 0) {
        return <p className="py-12 text-center text-sm text-zinc-500">No documents reviewed yet.</p>
    }

    return (
        <>
            <div className="divide-y divide-zinc-100">
                {documents.map((document) => (
                    <div key={document.id} className="group flex items-center gap-1 bg-white px-3 py-2">
                        <button
                            type="button"
                            onClick={() => onSelect(document)}
                            className="min-w-0 flex-1 grid grid-cols-[1fr_auto] grid-rows-2 gap-4 rounded-lg px-2 py-2.5 text-left transition hover:bg-zinc-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400"
                        >
                            <p className="col-start-1 row-start-1 truncate font-medium text-zinc-900">{displayName(document)}</p>
                            <div className="col-start-2 row-span-2 flex items-center justify-end">
                                <StatusBadge status={document.status} />
                            </div>
                            <p className="truncate text-sm text-zinc-500 col-start-1 row-start-2">
                                {document.original_filename}
                            </p>
                        </button>
                        <button
                            type="button"
                            onClick={() => setPendingDelete(document)}
                            aria-label={`Delete ${displayName(document)}`}
                            title="Delete document"
                            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-zinc-400 transition-colors hover:bg-red-50 hover:text-red-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-400"
                        >
                            <svg
                                aria-hidden="true"
                                width="16"
                                height="16"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.75"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M3 6h18" />
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
                                <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                            </svg>
                        </button>
                    </div>
                ))}
            </div>
            {pendingDelete && (
                <AlertDialog
                    open={Boolean(pendingDelete)}
                    onOpenChange={(open) => {
                        if (!open && !deleting) setPendingDelete(null)
                    }}
                >
                    <AlertDialogContent>
                        <AlertDialogHeader>
                            <AlertDialogTitle>
                                Delete {displayName(pendingDelete)}?
                            </AlertDialogTitle>
                            <AlertDialogDescription>
                                This removes the saved review and the uploaded file. This action cannot be undone.
                            </AlertDialogDescription>
                        </AlertDialogHeader>

                        <AlertDialogFooter>
                            <AlertDialogCancel disabled={deleting}>
                                Cancel
                            </AlertDialogCancel>

                            <AlertDialogAction
                                disabled={deleting}
                                onClick={(e) => {
                                    e.preventDefault()
                                    void remove()
                                }}
                                className="bg-red-600 text-white hover:bg-red-700 focus:ring-red-600"
                            >
                                {deleting ? 'Deleting…' : 'Delete'}
                            </AlertDialogAction>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialog>
            )}
        </>
    )
}