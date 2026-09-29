import type { Document } from '@/lib/types'

import { DocumentReview } from '@/components/DocumentReview'

interface ResultProps {
    selected: Document
    onChanged: (document: Document) => void
}

export function Result({ selected, onChanged }: Readonly<ResultProps>) {
    return (
        <main className="mx-auto max-w-5xl px-6 py-8">
            <div className="mb-6">
                <p className="text-sm text-zinc-500">Step 3 of 3</p>
                <h1 className="mt-1 text-2xl font-semibold tracking-tight">Review the result</h1>
                <p className="mt-1 text-sm text-zinc-600">
                    Correct fields if needed, then approve or reject.
                    For rejected reviews with supplier issues, a correction email draft can be generated.
                </p>
            </div>
            <DocumentReview
                key={selected.id}
                document={selected}
                onChanged={onChanged}
            />
        </main>
    )
}