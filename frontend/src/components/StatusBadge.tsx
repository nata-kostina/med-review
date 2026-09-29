import { Badge } from './ui/badge'

import type { DocumentStatus } from '../lib/types'

const labels: Record<DocumentStatus, string> = {
    processing: 'Processing',
    ready: 'Ready',
    needs_review: 'Needs review',
    approved: 'Approved',
    rejected: 'Rejected',
    failed: 'Failed',
}

const variants: Record<
    DocumentStatus,
  'default' | 'secondary' | 'outline' | 'success' | 'warning' | 'destructive'
> = {
    processing: 'secondary',
    ready: 'success',
    needs_review: 'warning',
    approved: 'success',
    rejected: 'destructive',
    failed: 'destructive',
}

export function StatusBadge({ status }: Readonly<{ status: DocumentStatus }>) {
    return <Badge className="" variant={variants[status]}>{labels[status]}</Badge>
}
