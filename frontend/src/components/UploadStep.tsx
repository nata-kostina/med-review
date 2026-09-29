import {
    useEffect,
    useRef,
    useState
} from 'react'

import { DocumentPreview } from './DocumentPreview'
import { Button } from './ui/button'
import {
    Card,
    CardContent,
    CardHeader
} from './ui/card'

import { createFilePreview } from '@/lib/file-preview'

interface UploadStepProps {
    file: File | null
    error: string | null
    onChoose: (file: File) => void
    onProcess: () => void
    onBack: () => void
}

const maxBytes = 4 * 1024 * 1024
const accepted = ['application/pdf']

export function UploadStep({
    file, error, onChoose, onProcess, onBack 
}: Readonly<UploadStepProps>) {
    const inputRef = useRef<HTMLInputElement>(null)
    const [localError, setLocalError] = useState<string | null>(null)

    function choose(next?: File) {
        if (!next) return
        if (!accepted.includes(next.type)) {
            setLocalError('Choose a PDF document.')
            return
        }
        if (next.size > maxBytes) {
            setLocalError('This demo accepts files up to 4 MB.')
            return
        }
        setLocalError(null)
        onChoose(next)
    }

    return (
        <main className="mx-auto max-w-6xl px-6 py-10">
            <div className="mb-6">
                <Button
                    onClick={onBack}
                    variant="ghost"
                    size="sm"
                    className="-ml-3"
                >
                    ← Back
                </Button>
                <div>
                    <p className="mt-5 text-sm text-zinc-500">Step 1 of 3</p>
                    <h1 className="mt-1 text-2xl font-semibold tracking-tight">Choose a document</h1>
                    <p className="mt-1 text-sm text-zinc-600">
                        Check the preview first. The file is only sent to Azure after you confirm.
                    </p>
                </div>
            </div>
            {(localError || error) && (
                <div role="alert" className="mt-5 mb-5 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">
                    {localError || error}
                </div>
            )}
            <div className={`grid gap-6 ${file ? 'lg:grid-cols-[1fr_360px]' : ''}`}>
                {file ? (
                    <SelectedFilePreview key={`${file.name}-${file.lastModified}`} file={file} />
                ) : (
                    <button
                        type="button"
                        onClick={() => inputRef.current?.click()}
                        onDragOver={(event) => event.preventDefault()}
                        onDrop={(event) => {
                            event.preventDefault()
                            choose(event.dataTransfer.files[0])
                        }}
                        className="flex min-h-[400px] w-full flex-col items-center justify-center rounded-xl border border-dashed border-zinc-300 bg-white p-10 text-center transition hover:border-zinc-500 hover:bg-zinc-50"
                    >
                        <span className="flex h-10 w-10 items-center justify-center rounded-lg border border-zinc-200 bg-zinc-50 text-lg text-zinc-600">
                            ↑
                        </span>
                        <span className="mt-4 font-medium">Drop a document here</span>
                        <span className="mt-1 text-sm text-zinc-500">or click to browse · PDF · maximum 4 MB</span>
                    </button>
                )}

                {file && (
                    <Card className="h-fit">
                        <CardHeader>
                            <p className="text-sm font-medium text-zinc-900">Ready to process</p>
                            <p className="break-all pt-2 text-sm font-medium">{file.name}</p>
                            <p className="text-sm text-zinc-500">
                                {(file.size / 1024).toFixed(0)} KB · {file.type || 'Unknown format'}
                            </p>
                        </CardHeader>
                        <CardContent>
                            <Button
                                onClick={() => inputRef.current?.click()}
                                variant="outline"
                                className="w-full"
                            >
                                Choose a different file
                            </Button>
                            <Button onClick={onProcess} className="mt-5 w-full">
                                Process document
                            </Button>
                        </CardContent>
                    </Card>
                )}
            </div>

            <input
                ref={inputRef}
                type="file"
                className="sr-only"
                accept={accepted.join(',')}
                onChange={(event) => choose(event.target.files?.[0])}
            />
        </main>
    )
}

function SelectedFilePreview({ file }: Readonly<{ file: File }>) {
    const [previewUrl, setPreviewUrl] = useState<string | null>(null)
    const [previewError, setPreviewError] = useState<string | null>(null)

    useEffect(() => {
        const preview = createFilePreview(file)
        void preview.result
            .then(setPreviewUrl)
            .catch((reason: unknown) => {
                if (reason instanceof DOMException && reason.name === 'AbortError') return
                setPreviewError(
                    reason instanceof Error ? reason.message : 'The selected file could not be previewed.',
                )
            })
        return preview.abort
    }, [file])

    if (previewError) {
        return (
            <div
                role="alert"
                className="flex min-h-130 items-center justify-center rounded-xl border border-red-200 bg-red-50 p-8 text-center text-sm text-red-800"
            >
                {previewError}
            </div>
        )
    }

    if (!previewUrl) {
        return (
            <div className="flex min-h-130 items-center justify-center rounded-xl border border-zinc-200 bg-white text-sm text-zinc-500">
                Preparing preview…
            </div>
        )
    }

    return <DocumentPreview src={previewUrl} filename={file.name} />
}