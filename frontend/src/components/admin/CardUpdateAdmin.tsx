import React, { useState, useEffect, useCallback } from 'react';
import {
  RefreshCw,
  Zap,
  Clock,
  CheckCircle2,
  AlertCircle,
  X,
  Play,
  FlaskConical,
  ChevronRight,
  Loader2,
} from 'lucide-react';
import axios, { AxiosRequestConfig } from 'axios';

type HttpMethod = 'get' | 'post';

interface ProgressEntryBase {
  card_id: number;
  card_name: string;
  bank_name: string;
}

interface CurrentProgress extends ProgressEntryBase {
  stage: string;
  position: number;
  total: number;
  [key: string]: any;
}

interface CompletedProgress extends ProgressEntryBase {
  status: string;
  suggestions_created: number;
  timestamp: string;
  meta: Record<string, any>;
}

interface UpdateStatus {
  is_running: boolean;
  scheduler_running: boolean;
  next_run: string | null;
  progress?: {
    total_cards: number;
    processed_cards: number;
    current?: CurrentProgress | null;
    last_completed?: CompletedProgress | null;
  };
  last_run_summary?: {
    total_cards: number;
    processed_cards: number;
    suggestions_created: number;
    skipped: number;
    failed: number;
    completed_at: string;
  } | null;
  last_error?: string | null;
}

interface TriggerCardForm { cardId: string; }
interface ExtractionForm { url: string; cardName: string; bankName: string; cardVariant: string; }

const API_BASE =
  process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === 'production'
    ? 'https://smartcards-ai-2.onrender.com/api/v1'
    : 'http://localhost:8000/api/v1');

// ── small reusable components ────────────────────────────────────────────────

const StatusBadge: React.FC<{ running: boolean }> = ({ running }) =>
  running ? (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">
      <Loader2 className="w-3 h-3 animate-spin" /> Running
    </span>
  ) : (
    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300">
      <CheckCircle2 className="w-3 h-3" /> Idle
    </span>
  );

const StageBadge: React.FC<{ stage: string }> = ({ stage }) => {
  const labels: Record<string, string> = {
    search: 'Discovering sources',
    fetch_official: 'Fetching page',
    extract: 'Extracting data',
    compare: 'Comparing with DB',
    suggestions_created: 'Suggestions created',
    no_change: 'No changes',
    no_official_source: 'No source found',
    fetch_failed: 'Fetch failed',
  };
  return (
    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-100 text-primary-700 dark:bg-primary-900/40 dark:text-primary-300">
      {labels[stage] ?? stage}
    </span>
  );
};

const Alert: React.FC<{ type: 'error' | 'success' | 'warning' | 'info'; message: string; onClose?: () => void }> = ({ type, message, onClose }) => {
  const styles = {
    error:   'bg-red-50 border-red-200 text-red-700 dark:bg-red-900/20 dark:border-red-800 dark:text-red-300',
    success: 'bg-green-50 border-green-200 text-green-700 dark:bg-green-900/20 dark:border-green-800 dark:text-green-300',
    warning: 'bg-amber-50 border-amber-200 text-amber-700 dark:bg-amber-900/20 dark:border-amber-800 dark:text-amber-300',
    info:    'bg-blue-50 border-blue-200 text-blue-700 dark:bg-blue-900/20 dark:border-blue-800 dark:text-blue-300',
  };
  const Icon = type === 'error' || type === 'warning' ? AlertCircle : CheckCircle2;
  return (
    <div className={`flex items-start gap-3 p-3.5 rounded-lg border text-sm ${styles[type]}`}>
      <Icon className="w-4 h-4 mt-0.5 flex-shrink-0" />
      <span className="flex-1">{message}</span>
      {onClose && (
        <button onClick={onClose} className="flex-shrink-0 opacity-60 hover:opacity-100">
          <X className="w-4 h-4" />
        </button>
      )}
    </div>
  );
};

const ProgressBar: React.FC<{ percent: number; active: boolean }> = ({ percent, active }) => (
  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
    <div
      className={`h-2 rounded-full transition-all duration-500 ${active ? 'bg-primary-500 animate-pulse' : 'bg-primary-500'}`}
      style={{ width: `${percent}%` }}
    />
  </div>
);

// ── Modal ────────────────────────────────────────────────────────────────────

const Modal: React.FC<{ open: boolean; title: string; onClose: () => void; children: React.ReactNode; width?: string }> = ({
  open, title, onClose, children, width = 'max-w-md',
}) => {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" onClick={onClose} />
      <div className={`relative w-full ${width} bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border border-gray-200 dark:border-gray-700`}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 className="text-base font-semibold text-gray-900 dark:text-white">{title}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  );
};

// ── Confirm Modal ─────────────────────────────────────────────────────────────

const ConfirmModal: React.FC<{
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  danger?: boolean;
  loading?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}> = ({ open, title, message, confirmLabel = 'Confirm', danger, loading, onConfirm, onCancel }) => (
  <Modal open={open} title={title} onClose={onCancel}>
    <p className="text-sm text-gray-600 dark:text-gray-300 mb-6">{message}</p>
    <div className="flex justify-end gap-3">
      <button
        onClick={onCancel}
        disabled={loading}
        className="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
      >
        Cancel
      </button>
      <button
        onClick={onConfirm}
        disabled={loading}
        className={`px-4 py-2 text-sm font-medium text-white rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2 ${
          danger
            ? 'bg-red-600 hover:bg-red-700'
            : 'bg-primary-600 hover:bg-primary-700'
        }`}
      >
        {loading && <Loader2 className="w-4 h-4 animate-spin" />}
        {confirmLabel}
      </button>
    </div>
  </Modal>
);

// ── Field ────────────────────────────────────────────────────────────────────

const Field: React.FC<{ label: string; required?: boolean; error?: string; children: React.ReactNode }> = ({ label, required, error, children }) => (
  <div className="space-y-1.5">
    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
      {label}{required && <span className="text-red-500 ml-1">*</span>}
    </label>
    {children}
    {error && <p className="text-xs text-red-500">{error}</p>}
  </div>
);

const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = (props) => (
  <input
    {...props}
    className={`w-full px-3 py-2.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 ${props.className ?? ''}`}
  />
);

// ── Stat box ─────────────────────────────────────────────────────────────────

const Stat: React.FC<{ label: string; value: React.ReactNode }> = ({ label, value }) => (
  <div>
    <p className="text-xs text-gray-400 dark:text-gray-500 uppercase tracking-wide font-medium mb-1">{label}</p>
    <p className="text-sm font-semibold text-gray-900 dark:text-white">{value}</p>
  </div>
);

// ── Main Component ────────────────────────────────────────────────────────────

export const CardUpdateAdmin: React.FC = () => {
  const [status, setStatus] = useState<UpdateStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Confirm modals
  const [confirmAllOpen, setConfirmAllOpen] = useState(false);
  const [confirmPortfolioOpen, setConfirmPortfolioOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);

  // Card modal
  const [cardModalOpen, setCardModalOpen] = useState(false);
  const [cardForm, setCardForm] = useState<TriggerCardForm>({ cardId: '' });
  const [cardFormError, setCardFormError] = useState('');

  // Extract modal
  const [extractModalOpen, setExtractModalOpen] = useState(false);
  const [extractForm, setExtractForm] = useState<ExtractionForm>({ url: '', cardName: '', bankName: '', cardVariant: '' });
  const [extractErrors, setExtractErrors] = useState<Partial<ExtractionForm>>({});

  const authRequest = useCallback(async <TResponse, TBody = any>(method: HttpMethod, url: string, data?: TBody): Promise<TResponse> => {
    const token = localStorage.getItem('access_token');
    if (!token) throw new Error('Authentication required. Please login again.');
    const config: AxiosRequestConfig = {
      method,
      url: `${API_BASE}${url}`,
      headers: { Authorization: `Bearer ${token}` },
    };
    if (data && method === 'post') config.data = data;
    try {
      const response = await axios.request<TResponse>(config);
      return response.data;
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.response?.data?.message || err?.message || 'Request failed';
      throw new Error(detail);
    }
  }, []);

  const fetchStatus = useCallback(async () => {
    setFetching(true);
    setError(null);
    try {
      const result = await authRequest<UpdateStatus>('get', '/card-updates/status');
      setStatus(result);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setFetching(false);
    }
  }, [authRequest]);

  useEffect(() => {
    fetchStatus();
    const id = window.setInterval(fetchStatus, 30000);
    return () => window.clearInterval(id);
  }, [fetchStatus]);

  useEffect(() => {
    if (!success) return;
    const t = window.setTimeout(() => setSuccess(null), 6000);
    return () => window.clearTimeout(t);
  }, [success]);

  useEffect(() => {
    if (!error) return;
    const t = window.setTimeout(() => setError(null), 6000);
    return () => window.clearTimeout(t);
  }, [error]);

  const fmt = (iso?: string | null) => {
    if (!iso) return '—';
    const d = new Date(iso);
    return isNaN(d.getTime()) ? '—' : d.toLocaleString();
  };

  const progress = status?.progress;
  const totalCards = progress?.total_cards ?? 0;
  const processedCards = progress?.processed_cards ?? 0;
  const progressPercent = totalCards > 0 ? Math.round((processedCards / totalCards) * 100) : 0;
  const currentCard = progress?.current ?? null;
  const lastCompleted = progress?.last_completed ?? null;

  // Trigger all
  const doTriggerAll = async () => {
    setConfirmLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await authRequest('post', '/card-updates/trigger-all', {});
      setSuccess('Bulk card update started in the background.');
      setConfirmAllOpen(false);
      await fetchStatus();
    } catch (e: any) {
      setError(e.message);
      setConfirmAllOpen(false);
    } finally {
      setConfirmLoading(false);
    }
  };

  // Trigger portfolio
  const doTriggerPortfolio = async () => {
    setConfirmLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const res = await authRequest<{ portfolio_cards: number }>('post', '/card-updates/trigger-portfolio', {});
      setSuccess(`Portfolio update started for ${res.portfolio_cards} cards.`);
      setConfirmPortfolioOpen(false);
      await fetchStatus();
    } catch (e: any) {
      setError(e.message);
      setConfirmPortfolioOpen(false);
    } finally {
      setConfirmLoading(false);
    }
  };

  // Trigger single card
  const handleTriggerCard = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cardForm.cardId || !/^\d+$/.test(cardForm.cardId)) {
      setCardFormError('Please enter a valid numeric card ID.');
      return;
    }
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const res = await authRequest<{ card_name?: string; suggestions_created?: number; message?: string }>('post', `/card-updates/trigger-card/${cardForm.cardId}`, {});
      const n = res.suggestions_created ?? 0;
      const base = res.message || `Update completed for ${res.card_name || `card #${cardForm.cardId}`}.`;
      setSuccess(`${base} ${n > 0 ? `${n} suggestion${n === 1 ? '' : 's'} ready for review.` : 'No new suggestions detected.'}`);
      setCardModalOpen(false);
      setCardForm({ cardId: '' });
      await fetchStatus();
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  // Test extraction
  const handleTestExtraction = async (e: React.FormEvent) => {
    e.preventDefault();
    const errs: Partial<ExtractionForm> = {};
    if (!extractForm.url) errs.url = 'Required';
    if (!extractForm.cardName) errs.cardName = 'Required';
    if (!extractForm.bankName) errs.bankName = 'Required';
    if (Object.keys(errs).length) { setExtractErrors(errs); return; }
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const data = await authRequest<{ content_length: number; extracted_data?: Record<string, unknown> }>('post', '/card-updates/extract-from-url', {
        url: extractForm.url,
        card_name: extractForm.cardName,
        bank_name: extractForm.bankName,
        card_variant: extractForm.cardVariant || undefined,
      });
      setSuccess(`Extraction successful. Content length: ${data.content_length}. Keys: ${Object.keys(data.extracted_data || {}).join(', ') || 'none'}`);
      setExtractModalOpen(false);
      setExtractForm({ url: '', cardName: '', bankName: '', cardVariant: '' });
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">

      {/* Alerts */}
      {error   && <Alert type="error"   message={error}   onClose={() => setError(null)} />}
      {success && <Alert type="success" message={success} onClose={() => setSuccess(null)} />}

      {/* Main card */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">

        {/* Card header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary-100 dark:bg-primary-900/40 rounded-lg">
              <Zap className="w-5 h-5 text-primary-600 dark:text-primary-400" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-gray-900 dark:text-white">Automated Card Updates</h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">AI-powered pipeline to keep card data current</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            <button
              onClick={fetchStatus}
              disabled={fetching}
              className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${fetching ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={() => setConfirmPortfolioOpen(true)}
              disabled={loading || status?.is_running}
              className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-primary-600 dark:text-primary-400 border border-primary-300 dark:border-primary-700 rounded-lg hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors disabled:opacity-50"
            >
              <Play className="w-4 h-4" />
              Portfolio Cards
            </button>
            <button
              onClick={() => setConfirmAllOpen(true)}
              disabled={loading || status?.is_running}
              className="flex items-center gap-1.5 px-3 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50"
            >
              <Zap className="w-4 h-4" />
              Update All Cards
            </button>
          </div>
        </div>

        {/* Status section */}
        <div className="p-6 space-y-5">

          {/* Status row */}
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Status:</span>
            {status ? <StatusBadge running={status.is_running} /> : <span className="text-sm text-gray-400">Loading...</span>}
          </div>

          {/* Stats grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-gray-50 dark:bg-gray-700/40 rounded-xl border border-gray-100 dark:border-gray-700">
            <Stat label="Scheduler"     value={status?.scheduler_running ? 'Active' : 'Stopped'} />
            <Stat label="Next Run"      value={fmt(status?.next_run)} />
            <Stat label="This Run"      value={status?.is_running ? `${processedCards} / ${totalCards || '?'}` : '—'} />
            <Stat label="Suggestions"   value={status?.last_run_summary ? status.last_run_summary.suggestions_created : '—'} />
          </div>

          {/* Last error */}
          {status?.last_error && (
            <Alert type="warning" message={`Last run issue: ${status.last_error}`} />
          )}

          {/* Active progress */}
          {status?.is_running && totalCards > 0 && (
            <div className="space-y-3 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-100 dark:border-blue-800">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium text-blue-700 dark:text-blue-300">Processing…</span>
                <span className="text-blue-600 dark:text-blue-400">{progressPercent}%</span>
              </div>
              <ProgressBar percent={progressPercent} active />
              {currentCard && (
                <div className="flex items-center gap-2 text-sm text-blue-700 dark:text-blue-300">
                  <ChevronRight className="w-4 h-4 flex-shrink-0" />
                  <span>{currentCard.bank_name} {currentCard.card_name}</span>
                  <StageBadge stage={currentCard.stage} />
                </div>
              )}
              {lastCompleted && (
                <p className="text-xs text-blue-500 dark:text-blue-400">
                  Last completed: {lastCompleted.bank_name} {lastCompleted.card_name} — {lastCompleted.suggestions_created} suggestion{lastCompleted.suggestions_created !== 1 ? 's' : ''}
                </p>
              )}
            </div>
          )}

          {/* Last run summary */}
          {status?.last_run_summary && (
            <div>
              <p className="text-xs text-gray-400 dark:text-gray-500 uppercase tracking-wide font-medium mb-3">Last Run Summary</p>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-gray-50 dark:bg-gray-700/40 rounded-xl border border-gray-100 dark:border-gray-700">
                <Stat label="Completed"  value={fmt(status.last_run_summary.completed_at)} />
                <Stat label="Processed"  value={`${status.last_run_summary.processed_cards} / ${status.last_run_summary.total_cards}`} />
                <Stat label="Skipped"    value={status.last_run_summary.skipped} />
                <Stat label="Failed"     value={status.last_run_summary.failed} />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Manual Tools card */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3 px-6 py-5 border-b border-gray-200 dark:border-gray-700">
          <div className="p-2 bg-purple-100 dark:bg-purple-900/40 rounded-lg">
            <FlaskConical className="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-gray-900 dark:text-white">Manual Tools</h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">Update a specific card or test extraction from a URL</p>
          </div>
        </div>
        <div className="p-6 flex flex-wrap gap-3">
          <button
            onClick={() => setCardModalOpen(true)}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
          >
            <Play className="w-4 h-4" />
            Trigger One Card
          </button>
          <button
            onClick={() => setExtractModalOpen(true)}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
          >
            <FlaskConical className="w-4 h-4" />
            Test Extraction
          </button>
        </div>
      </div>

      {/* ── Confirm Modals ── */}
      <ConfirmModal
        open={confirmAllOpen}
        title="Update All Cards?"
        message="This will start the automated update pipeline for every active card in the database. The task runs in the background and may take several minutes."
        confirmLabel="Update All"
        danger
        loading={confirmLoading}
        onConfirm={doTriggerAll}
        onCancel={() => setConfirmAllOpen(false)}
      />
      <ConfirmModal
        open={confirmPortfolioOpen}
        title="Update Portfolio Cards?"
        message="This will update only cards that users have added to their portfolios (at least one active holder). The task runs in the background."
        confirmLabel="Start Portfolio Update"
        loading={confirmLoading}
        onConfirm={doTriggerPortfolio}
        onCancel={() => setConfirmPortfolioOpen(false)}
      />

      {/* ── Trigger One Card Modal ── */}
      <Modal open={cardModalOpen} title="Trigger Single Card Update" onClose={() => { setCardModalOpen(false); setCardForm({ cardId: '' }); setCardFormError(''); }}>
        <form onSubmit={handleTriggerCard} className="space-y-5">
          <Field label="Card ID" required error={cardFormError}>
            <Input
              type="text"
              inputMode="numeric"
              placeholder="e.g. 42"
              value={cardForm.cardId}
              onChange={e => { setCardForm({ cardId: e.target.value }); setCardFormError(''); }}
            />
          </Field>
          <div className="flex justify-end gap-3">
            <button type="button" onClick={() => setCardModalOpen(false)} className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors disabled:opacity-50">
              {loading && <Loader2 className="w-4 h-4 animate-spin" />}
              Trigger Update
            </button>
          </div>
        </form>
      </Modal>

      {/* ── Test Extraction Modal ── */}
      <Modal open={extractModalOpen} title="Test Extraction From URL" width="max-w-lg" onClose={() => { setExtractModalOpen(false); setExtractForm({ url: '', cardName: '', bankName: '', cardVariant: '' }); setExtractErrors({}); }}>
        <form onSubmit={handleTestExtraction} className="space-y-4">
          <Field label="Bank URL" required error={extractErrors.url}>
            <Input
              type="url"
              placeholder="https://www.bank.com/cards/hdfc-regalia"
              value={extractForm.url}
              onChange={e => { setExtractForm(p => ({ ...p, url: e.target.value })); setExtractErrors(p => ({ ...p, url: '' })); }}
            />
          </Field>
          <Field label="Card Name" required error={extractErrors.cardName}>
            <Input
              type="text"
              placeholder="Regalia Credit Card"
              value={extractForm.cardName}
              onChange={e => { setExtractForm(p => ({ ...p, cardName: e.target.value })); setExtractErrors(p => ({ ...p, cardName: '' })); }}
            />
          </Field>
          <Field label="Bank Name" required error={extractErrors.bankName}>
            <Input
              type="text"
              placeholder="HDFC Bank"
              value={extractForm.bankName}
              onChange={e => { setExtractForm(p => ({ ...p, bankName: e.target.value })); setExtractErrors(p => ({ ...p, bankName: '' })); }}
            />
          </Field>
          <Field label="Card Variant (optional)">
            <Input
              type="text"
              placeholder="e.g. Visa Signature"
              value={extractForm.cardVariant}
              onChange={e => setExtractForm(p => ({ ...p, cardVariant: e.target.value }))}
            />
          </Field>
          <div className="flex justify-end gap-3 pt-1">
            <button type="button" onClick={() => setExtractModalOpen(false)} className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors disabled:opacity-50">
              {loading && <Loader2 className="w-4 h-4 animate-spin" />}
              Run Extraction
            </button>
          </div>
        </form>
      </Modal>

      {/* scheduler status */}
      {status && (
        <p className="text-xs text-center text-gray-400 dark:text-gray-500">
          <Clock className="w-3 h-3 inline mr-1" />
          Next scheduled run: {fmt(status.next_run)}
        </p>
      )}
    </div>
  );
};

export default CardUpdateAdmin;
