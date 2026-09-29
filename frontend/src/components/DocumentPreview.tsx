interface DocumentPreviewProps {
    src: string
    filename: string
    className?: string
}

export function DocumentPreview({
    src, filename, className = '' 
}: DocumentPreviewProps) {
    const frameClass = `h-full min-h-[520px] w-full rounded-xl border border-zinc-200 bg-zinc-100 ${className}`

    return (
        <div className={`${frameClass} overflow-hidden`}>
            <iframe
                src={src}
                title={`Source document: ${filename}`}
                className="h-full min-h-[520px] w-full border-0 bg-white"
            />
        </div>
    )
}
