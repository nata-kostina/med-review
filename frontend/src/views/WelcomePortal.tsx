import { Button } from '@/components/ui/button'
import {
    Card,
    CardContent,
    CardHeader
} from '@/components/ui/card'

interface WelcomePortalProps {
    onStart: () => void
    onHistory: () => void
}

const steps = [
    [
        '1',
        'Upload a document',
        'Choose a medical document and check the preview.'
    ],
    [
        '2',
        'Run the pipeline',
        'Extract patient\'s information.'
    ],
    [
        '3',
        'Inspect the result',
        'Review extraction and findings.'
    ],
]

function WelcomePortal({ onStart, onHistory }: Readonly<WelcomePortalProps>) {
    return (
        <main className="mx-auto flex min-h-screen max-w-3xl items-center px-6 py-12">
            <Card className="w-full">
                <CardHeader className="border-b border-zinc-100 p-8 sm:p-10">
                    <p className="text-sm font-medium text-zinc-500">LabTest Diagnostics</p>
                    <h1 className="pt-2 text-3xl font-semibold tracking-tight text-zinc-950">Document review</h1>
                    <p className="max-w-xl pt-1 text-base leading-7 text-zinc-600">
                        Upload a medical document, run the review pipeline, and inspect the prepared result before
                        bookkeeping.
                    </p>
                    <div className="flex flex-wrap gap-3 pt-5">
                        <Button onClick={onStart}>Review a document</Button>
                        <Button onClick={onHistory} variant="outline">
                            View history
                        </Button>
                    </div>
                </CardHeader>
                <CardContent className="p-8 sm:p-10">
                    <h2 className="text-sm font-medium text-zinc-900">How it works</h2>
                    <ol className="mt-5 divide-y divide-zinc-100">
                        {steps.map(([
                            number,
                            title,
                            copy
                        ]) => (
                            <li
                                key={number}
                                className="grid items-center gap-2 py-4 first:pt-0 last:pb-0 sm:grid-cols-[32px_160px_1fr] sm:items-center"
                            >
                                <span className="flex h-7 w-7 items-center justify-center rounded-md bg-zinc-100 text-xs font-medium text-zinc-700">
                                    {number}
                                </span>
                                <span className="text-sm font-medium text-zinc-900">{title}</span>
                                <span className="text-sm leading-6 text-zinc-500">{copy}</span>
                            </li>
                        ))}
                    </ol>
                </CardContent>
            </Card>
        </main>
    )
}

export default WelcomePortal