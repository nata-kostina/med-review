import { useState } from 'react'

import { CorrectionEmailDialog } from './CorrectionEmailDialog'
import { DocumentReviewSection } from './DocumentReviewSection'
import { StatusBadge } from './StatusBadge'
import { Badge } from './ui/badge'
import { Button } from './ui/button'

import type {
    CorrectionEmailDraft,
    Document,
    ReviewData
} from '@/lib/types'

import { api } from '@/api'
import { summarizeReview } from '@/lib/review-outcome'

interface DocumentReviewProps {
    document: Document
    onChanged: (document: Document) => void
}

function shown(value: string | null | undefined): string {
    return value?.trim() || 'Not found'
}

type EditableField = keyof ReviewData

const fieldGroups: Array<{ title: string;
    fields: Array<{ key: EditableField;
        label: string;
        type?: string }> }> = [
    {
        title: 'General',
        fields: [
            {
                key: 'recorded_date',
                label: 'Recorded Date',
                type: 'date' 
            },
        ]
    },
    {
        title: 'Patient details',
        fields: [
            {
                key: 'patient_name',
                label: 'Patient name' 
            },
            {
                key: 'age',
                label: 'Age' 
            },
            {
                key: 'dob',
                label: 'Date of birth',
                type: 'date' 
            },
            {
                key: 'diagnosis',
                label: 'Diagnosis' 
            },
            {
                key: 'sex',
                label: 'Sex' 
            },
            {
                key: 'ssn',
                label: 'SSN' 
            },
        ],
    },
    {
        title: 'Hospital details',
        fields: [
            {
                key: 'hospital',
                label: 'Hospital' 
            },
            {
                key: 'doctor_name',
                label: 'Doctor name' 
            },
            {
                key: 'doctor_id',
                label: 'Doctor ID' 
            },
        ],
    },
]

export function DocumentReview({ document, onChanged }: Readonly<DocumentReviewProps>) {
    const [draft, setDraft] = useState<ReviewData | null>(document.review_data)
    const outcome = summarizeReview(document.status, document.issues)
    const outcomeStyle = {
        passed: 'border-emerald-200 bg-emerald-50 text-emerald-950',
        attention: 'border-amber-200 bg-amber-50 text-amber-950',
        in_progress: 'border-amber-200 bg-amber-50 text-amber-950',
        failed: 'border-red-200 bg-red-50 text-red-950',
    }[outcome.kind]
    const outcomeBadge = {
        passed: 'success',
        attention: 'warning',
        in_progress: 'warning',
        failed: 'destructive',
    }[outcome.kind] as 'success' | 'warning' | 'destructive'
    const locked = document.status === 'approved' || document.status === 'rejected'
    const [busy, setBusy] = useState<'save' | 'account' | 'approved' | 'rejected' | null>(null)
    const [dirty, setDirty] = useState(false)
    const [error, setError] = useState<string | null>(null)
    const hasErrors = document.issues.some((issue) => issue.severity === 'error')
    const [emailOpen, setEmailOpen] = useState(false)
    const [emailLoading, setEmailLoading] = useState(false)
    const [emailDraft, setEmailDraft] = useState<CorrectionEmailDraft | null>(null)
    const [emailError, setEmailError] = useState<string | null>(null)

    const summary = [
        {
            key: 'patient_name',
            label: 'Patient Name',
            value: shown(document.review_data?.patient_name) 
        },
        {
            key: 'doctor_name',
            label: 'Doctor Name',
            value: shown(document.review_data?.doctor_name) 
        },
        {
            key: 'doctor_id',
            label: 'Doctor ID',
            value: shown(document.review_data?.doctor_id) 
        },
        {
            key: 'hospital',
            label: 'Hospital',
            value: shown(document.review_data?.hospital) 
        },
        {
            key: 'recorded_date',
            label: 'Recorded Date',
            value: shown(document.review_data?.recorded_date) 
        },
        {
            key: 'age',
            label: 'Age',
            value: shown(document.review_data?.age) 
        },
        {
            key: 'dob',
            label: 'Date of Birth',
            value: shown(document.review_data?.dob) 
        },
        {
            key: 'diagnosis',
            label: 'Diagnosis',
            value: shown(document.review_data?.diagnosis) 
        },
        {
            key: 'sex',
            label: 'Sex',
            value: shown(document.review_data?.sex) 
        },
        {
            key: 'ssn',
            label: 'SSN',
            value: shown(document.review_data?.ssn) 
        },
    ]

    function change(key: EditableField, value: string) {
        setDraft((current) => current ? {
            ...current,
            [key]: value || null 
        } : current)
        setDirty(true)
    }

    async function save() {
        if (!draft) return
        setBusy('save')
        setError(null)
        try {
             
            const {
                // eslint-disable-next-line @typescript-eslint/no-unused-vars
                field_confidence, field_sources, ...payload 
            } = draft
            const changed = await api.updateDocument(document.id, payload)
            setDraft(changed.review_data)
            setDirty(false)
            onChanged(changed)
        } catch (reason) {
            setError(reason instanceof Error ? reason.message : 'Could not save the correction.')
        } finally {
            setBusy(null)
        }
    }

    async function draftCorrectionEmail() {
        setEmailOpen(true)
        setEmailLoading(true)
        setEmailDraft(null)
        setEmailError(null)
        try {
            setEmailDraft(await api.generateCorrectionEmail(document.id))
        } catch (reason) {
            setEmailError(reason instanceof Error ? reason.message : 'Could not draft the correction email.')
        } finally {
            setEmailLoading(false)
        }
    }

    async function decide(decision: 'approved' | 'rejected') {
        setBusy(decision)
        setError(null)
        try {
            onChanged(await api.decideDocument(document.id, decision))
        } catch (reason) {
            setError(reason instanceof Error ? reason.message : 'Could not save the decision.')
        } finally {
            setBusy(null)
        }
    }

    const handleDecide = async (action: 'approved' | 'rejected') => {
        await decide(action)

        window.scrollTo({
            top: 0,
            behavior: 'smooth',
        })
    }

    return (

        <div className="overflow-hidden rounded-xl border border-zinc-200 bg-white shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-4 border-b border-zinc-100 px-6 py-4">
                <div>
                    <div className="flex flex-wrap items-center gap-2">
                        <p className="text-sm text-zinc-500">{document.original_filename}</p>
                    </div>
                    <h2 className="mt-1 text-lg font-semibold">{document.review_data?.patient_name ?? document.original_filename}</h2>
                </div>
                <StatusBadge status={document.status} />
            </div>

            <div className="space-y-8 p-6 sm:p-8">
                <section className={`rounded-xl border p-5 ${outcomeStyle}`}>
                    <div className="flex flex-wrap items-start justify-between gap-4">
                        <div>
                            <p className="text-lg font-semibold">{outcome.title}</p>
                            <p className="mt-1 text-sm leading-6 opacity-80">{outcome.description}</p>
                        </div>
                        <div className="flex gap-2">
                            {outcome.errorCount > 0 && <Badge variant="destructive">{outcome.errorCount} {outcome.errorCount === 1 ? 'error' : 'errors'}</Badge>}
                            {outcome.warningCount > 0 && <Badge variant="warning">{outcome.warningCount} {outcome.warningCount === 1 ? 'warning' : 'warnings'}</Badge>}
                            {outcome.errorCount === 0 && outcome.warningCount === 0 && <Badge variant={outcomeBadge}>{
                                outcome.kind === 'failed' ? 'Failed' :
                                    outcome.kind === 'passed' ? 'Passed' :
                                        'In Progress'
                            }</Badge>}
                        </div>
                    </div>
                </section>

                {document.error_message && (
                    <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800">{document.error_message}</div>
                )}

                {document.review_data && (
                    <section>
                        <div>
                            <h3 className="text-base font-semibold text-zinc-900">Document summary</h3>
                            <p className="mt-1 text-sm text-zinc-500">The combined values used for this review.</p>
                        </div>
                        <dl className="mt-4 grid overflow-hidden rounded-xl border border-zinc-200 sm:grid-cols-2 lg:grid-cols-4">
                            {summary.map((item) => (
                                <div key={item.key} className="border-b border-zinc-100 p-4 last:border-b-0 sm:border-r sm:[&:nth-last-child(-n+2)]:border-b-0 sm:[&:nth-child(2n)]:border-r-0 lg:[&:nth-last-child(-n+4)]:border-b-0 lg:[&:nth-child(2n)]:border-r lg:[&:nth-child(4n)]:border-r-0">
                                    <dt className="text-xs font-medium text-zinc-500">{item.label}</dt>
                                    <dd className="mt-1 break-words text-sm font-medium text-zinc-900">{item.value}</dd>
                                    {document.review_data?.field_sources?.[item.key] === 'llm_fallback' && <Badge variant="secondary" className="mt-2">LLM fallback</Badge>}
                                    {document.review_data?.field_sources?.[item.key] === 'human' && <Badge variant="secondary" className="mt-2">Human correction</Badge>}
                                </div>
                            ))}
                        </dl>
                    </section>
                )}

                {outcome.kind !== 'in_progress' && (<section className="border-t border-zinc-100 pt-7">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                        <div>
                            <h3 className="text-base font-semibold text-zinc-900">Automatic checks</h3>
                            <p className="mt-1 text-sm text-zinc-500">Deterministic rules decide whether this review can be approved.</p>
                        </div>
                        <Badge variant={outcomeBadge}>{document.issues.length} {document.issues.length === 1 ? 'issue' : 'issues'}</Badge>
                    </div>

                    {document.issues.length ? (
                        <ul className="mt-4 grid gap-2 sm:grid-cols-2">
                            {document.issues.map((issue) => (
                                <li key={`${issue.code}-${issue.field}`} className={`rounded-lg border p-3 text-sm ${issue.severity === 'error' ? 'border-red-200 bg-red-50 text-red-800' : 'border-amber-200 bg-amber-50 text-amber-900'}`}>
                                    <span className="font-semibold capitalize">{issue.severity}:</span> {issue.message}
                                </li>
                            ))}
                        </ul>
                    ) : document.status !== 'failed' && (
                        <p className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-800">No issues were found.</p>
                    )}
                </section>)}

                {document.status !== 'failed' && document.supplier_action_required && (
                    <section className="flex flex-col gap-4 rounded-xl border border-zinc-200 bg-zinc-50 p-5 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                            <h3 className="text-sm font-semibold text-zinc-900">Supplier action needed</h3>
                            <p className="mt-1 text-sm leading-6 text-zinc-600">Turn the business issues into a correction request you can copy into email.</p>
                        </div>
                        <Button variant="outline" onClick={() => void draftCorrectionEmail()}>Draft correction email</Button>
                    </section>
                )}

                {document.review && <DocumentReviewSection review={document.review} />}

                {draft && (
                    <section className="border-t border-zinc-100 pt-7">
                        <h3 className="text-base font-semibold text-zinc-900">Review extracted fields</h3>
                        <p className="mt-1 text-sm text-zinc-500">Correct anything that Azure read incorrectly, then rerun the checks.</p>
                        <form onSubmit={(event) => { event.preventDefault(); void save() }} className="mt-6 space-y-7">
                            {fieldGroups.map((group) => (
                                <fieldset key={group.title} disabled={locked || busy !== null}>
                                    <legend className="text-sm font-medium text-zinc-900">{group.title}</legend>
                                    <div className="mt-3 grid gap-4 sm:grid-cols-2">
                                        {group.fields.map((field) => (
                                            <label key={field.key} className="block text-sm font-medium text-zinc-700">
                                                {field.label}
                                                <input
                                                    type={field.type ?? 'text'}
                                                    step={field.type === 'number' ? '0.01' : undefined}
                                                    value={String(draft[field.key] ?? '')}
                                                    onChange={(event) => change(field.key, event.target.value)}
                                                    className="mt-1.5 w-full rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 outline-none focus:border-zinc-500 focus:ring-2 focus:ring-zinc-200 disabled:bg-zinc-100 disabled:text-zinc-500"
                                                />
                                            </label>
                                        ))}
                                    </div>
                                </fieldset>
                            ))}

                            {!locked && (
                                <Button
                                    type="submit"
                                    disabled={busy !== null}
                                    variant="outline"
                                >
                                    {busy === 'save' ? 'Rechecking…' : 'Save and rerun checks'}
                                </Button>
                            )}
                        </form>
                    </section>
                )}
                {error && <div role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{error}</div>}

                {!locked && document.status !== 'failed' && document.status !== 'processing' && (
                    <div className="border-t border-zinc-100 pt-6">
                        {dirty && <p className="mb-3 text-right text-sm text-amber-700">Save and rerun the checks before making a decision.</p>}
                        <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
                            <Button
                                disabled={busy !== null || dirty}
                                onClick={() => void handleDecide('rejected')}
                                variant="destructive"
                                className="sm:min-w-28"
                            >
                                {busy === 'rejected' ? 'Rejecting…' : 'Reject'}
                            </Button>
                            <Button
                                variant="success"
                                disabled={busy !== null || dirty || hasErrors}
                                onClick={() => void handleDecide('approved')}
                                title={dirty ? 'Save field changes before approval' : hasErrors ? 'Resolve validation errors before approval' : undefined}
                                className="sm:min-w-28"
                            >
                                {busy === 'approved' ? 'Approving…' : 'Approve'}
                            </Button>
                        </div>
                    </div>
                )}
            </div>
            {emailOpen && (
                <CorrectionEmailDialog
                    open
                    draft={emailDraft}
                    loading={emailLoading}
                    error={emailError}
                    onClose={() => setEmailOpen(false)}
                />
            )}
        </div>
    )
}