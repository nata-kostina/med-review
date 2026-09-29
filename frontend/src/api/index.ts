import { realDocumentApi } from './api'
import { mockDocumentApi } from './mockApi'

const IS_MOCK = import.meta.env.VITE_USE_MOCKS === 'true'

export const api = IS_MOCK ? mockDocumentApi : realDocumentApi