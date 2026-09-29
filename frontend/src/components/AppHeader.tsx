import { Button } from './ui/button'

interface AppHeaderProps {
    onHome: () => void
    onNew: () => void
    onHistory: () => void
}

export function AppHeader({
    onHistory, onHome, onNew 
}: Readonly<AppHeaderProps>) {
    return (
        <header className="border-b border-zinc-200 bg-white">
            <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
                <button
                    type="button"
                    onClick={onHome}
                    className="text-left"
                >
                    <p className="font-semibold text-zinc-950">Document review</p>
                    <p className="text-xs text-zinc-500">LabTest Diagnostics</p>
                </button>
                <nav className="flex items-center gap-2" aria-label="Application">
                    <Button
                        onClick={onHistory}
                        variant="ghost"
                        size="sm"
                    >
                        History
                    </Button>
                    <Button onClick={onNew} size="sm">
                        New review
                    </Button>
                </nav>
            </div>
        </header>
    )
}