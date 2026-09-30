declare global {
    interface Window {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        ym?: (counterId: number, action: string, ...args: any[]) => void
    }
}

export function targetYM(t: string | undefined): void {
    if (!t) return
    if (typeof window.ym === 'function') {
        window.ym(113218329, 'reachGoal', t)
    }
}
