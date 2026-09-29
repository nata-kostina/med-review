export const PROCESSING_STEPS = [
    {
        title: 'Extract and cross-check',
        description: 'Running Document Intelligence, then filling gaps from the independent LLM review.',
    },
    {
        title: 'Validate LabTest Diagnostics policy',
        description: 'Applying deterministic rules.',
    },
] as const

export function processingStepAt(elapsedMs: number): number {
    if (elapsedMs >= 4500) return 1
    return 0
}
