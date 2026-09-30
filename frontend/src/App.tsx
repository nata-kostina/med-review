import { useState } from 'react'

import { api } from './api'
import { AppHeader } from './components/AppHeader'
import { ProcessingStep } from './components/ProcessingStep'
import { UploadStep } from './components/UploadStep'
import { targetYM } from './lib/ym'
import { History } from './views/History'
import { Result } from './views/Result'
import WelcomePortal from './views/WelcomePortal'

import type { Document } from './lib/types'

type View = 'welcome' | 'upload' | 'processing' | 'result' | 'history'

function App() {
    const [view, setView] = useState<View>('welcome')
    const [file, setFile] = useState<File | null>(null)
    const [error, setError] = useState<string | null>(null)
    const [selected, setSelected] = useState<Document | null>(null)
    const [historyLoading, setHistoryLoading] = useState(false)
    const [documents, setDocuments] = useState<Document[]>([])

    function home() {
        setError(null)
        setView('welcome')
    }

    function startReview() {
        targetYM('click-review')
        setFile(null)
        setSelected(null)
        setError(null)
        setView('upload')
    }

    async function openHistory() {
        targetYM('click-history')
        setView('history')
        setError(null)
        setHistoryLoading(true)
        try {
            const documents = await api.listDocuments()
            setDocuments(documents)
        } catch (reason) {
            setError(reason instanceof Error ? reason.message : 'Could not load review history.')
        } finally {
            setHistoryLoading(false)
        }
    }

    async function removeHistoryDocument(next: Document) {
        setError(null)
        try {
            await api.deleteDocument(next.id)
            setDocuments((current) => current.filter((item) => item.id !== next.id))
            if (selected?.id === next.id) {
                setSelected(null)
            }
        } catch (reason) {
            const message = reason instanceof Error ? reason.message : 'Could not delete the document.'
            setError(message)
            throw reason
        }
    }

    function showDocument(next: Document) {
        setSelected(next)
        setView('result')
    }

    function handleChanged(changed: Document) {
        setSelected(changed)
        setDocuments((current) =>
            current.map((item) => (item.id === changed.id ? changed : item)),)
    }

    async function processDocument() {
        if (!file) return
        targetYM('click-process-document')
        setError(null)
        setView('processing')
        try {
            const processed = await api.uploadDocument(file)
            setSelected(processed)
            setDocuments((current) => [processed, ...current.filter((item) => item.id !== processed.id)])
            setView('result')
        } catch (reason) {
            setError(reason instanceof Error ? reason.message : 'Could not process the document.')
            setView('upload')
        }
    }

    return (
        <div className="min-h-screen bg-zinc-50 text-zinc-950">
            {view !== 'welcome' && (
                <AppHeader
                    onHome={home}
                    onNew={startReview}
                    onHistory={() => void openHistory()}
                />
            )}
            {view === 'welcome' && (
                <WelcomePortal
                    onStart={startReview}
                    onHistory={() => void openHistory()}
                />
            )}
            {view === 'upload' && (
                <UploadStep
                    file={file}
                    error={error}
                    onChoose={(next: File) => {
                        setFile(next)
                        setError(null)
                    }}
                    onProcess={() => void processDocument()}
                    onBack={home}
                />
            )}
            {view === 'processing' && file && <ProcessingStep filename={'file.name'} />}
            {view === 'history' && (
                <History
                    documents={documents}
                    error={error}
                    historyLoading={historyLoading}
                    onDelete={removeHistoryDocument}
                    onSelect={showDocument}
                />
            )}
            {view === 'result' && selected && (
                <Result
                    selected={selected}
                    onChanged={handleChanged}
                />
            )}
        </div>
    )
}

export default App