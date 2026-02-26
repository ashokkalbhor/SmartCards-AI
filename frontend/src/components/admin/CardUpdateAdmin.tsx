import React, { useState, useEffect, useCallback } from 'react';
import {
  Button,
  Card,
  Alert,
  Spin,
  Modal,
  Form,
  Input,
  Space,
  Tag,
  Progress,
} from 'antd';
import {
  ReloadOutlined,
  ThunderboltOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExperimentOutlined,
} from '@ant-design/icons';
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

interface TriggerCardPayload {
  cardId: string;
}

interface ExtractionPayload {
  url: string;
  cardName: string;
  bankName: string;
  cardVariant?: string;
}

const API_BASE =
  process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === 'production'
    ? 'https://smartcards-ai-2.onrender.com/api/v1'
    : 'http://localhost:8000/api/v1');

export const CardUpdateAdmin: React.FC = () => {
  const [status, setStatus] = useState<UpdateStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showCardModal, setShowCardModal] = useState(false);
  const [showExtractModal, setShowExtractModal] = useState(false);
  const [cardForm] = Form.useForm<TriggerCardPayload>();
  const [extractForm] = Form.useForm<ExtractionPayload>();

  const authRequest = useCallback(
    async <TResponse, TBody = any>(
      method: HttpMethod,
      url: string,
      data?: TBody
    ): Promise<TResponse> => {
      const resolvedToken = localStorage.getItem('access_token');
      if (!resolvedToken) {
        throw new Error('Authentication required. Please login again.');
      }

      const config: AxiosRequestConfig = {
        method,
        url: `${API_BASE}${url}`,
        headers: {
          Authorization: `Bearer ${resolvedToken}`,
        },
      };

      if (data && method === 'post') {
        config.data = data;
      }

      try {
        const response = await axios.request<TResponse>(config);
        return response.data;
      } catch (requestError: any) {
        const detail =
          requestError?.response?.data?.detail ||
          requestError?.response?.data?.message ||
          requestError?.message ||
          'Request failed';
        throw new Error(detail);
      }
    },
    []
  );

  const fetchStatus = useCallback(async () => {
    setFetching(true);
    setError(null);
    try {
      const result = await authRequest<UpdateStatus>('get', '/card-updates/status');
      setStatus(result);
    } catch (statusError: any) {
      setError(statusError.message);
    } finally {
      setFetching(false);
    }
  }, [authRequest]);

  useEffect(() => {
    fetchStatus();
    const interval = window.setInterval(fetchStatus, 30000);
    return () => window.clearInterval(interval);
  }, [fetchStatus]);

  const formattedDate = (isoDate?: string | null) => {
    if (!isoDate) return 'Not available';
    const parsed = new Date(isoDate);
    if (Number.isNaN(parsed.getTime())) return 'Not available';
    return parsed.toLocaleString();
  };

  const stageLabel = (stage?: string) => {
    switch (stage) {
      case 'search':
        return 'Discovering sources';
      case 'fetch_official':
        return 'Fetching official content';
      case 'extract':
        return 'Extracting structured data';
      case 'compare':
        return 'Comparing with database';
      case 'suggestions_created':
        return 'Suggestions created';
      case 'no_change':
        return 'No changes detected';
      case 'no_official_source':
        return 'No official source found';
      case 'fetch_failed':
        return 'Failed to fetch content';
      default:
        return stage ?? 'Working';
    }
  };

  const progress = status?.progress;
  const totalCards = progress?.total_cards ?? 0;
  const processedCards = progress?.processed_cards ?? 0;
  const progressPercent =
    totalCards > 0 ? Math.round((processedCards / totalCards) * 100) : 0;
  const currentCard = progress?.current ?? null;
  const lastCompleted = progress?.last_completed ?? null;

  const handleTriggerAll = () => {
    Modal.confirm({
      title: 'Trigger Update for All Cards?',
      icon: <ThunderboltOutlined />,
      content:
        'This will start the automated update process for every active card. The task runs in the background and may take several minutes.',
      okText: 'Trigger',
      cancelText: 'Cancel',
      okButtonProps: { type: 'primary', danger: true },
      onOk: async () => {
        setLoading(true);
        setError(null);
        setSuccess(null);
        try {
          await authRequest('post', '/card-updates/trigger-all', {});
          setSuccess('Bulk card update started.');
          await fetchStatus();
        } catch (triggerError: any) {
          setError(triggerError.message);
        } finally {
          setLoading(false);
        }
      },
    });
  };

  const handleTriggerPortfolio = () => {
    Modal.confirm({
      title: 'Trigger Update for Portfolio Cards?',
      icon: <ThunderboltOutlined />,
      content:
        'This will update only cards that users have added to their portfolios (cards with at least one active holder). The task runs in the background.',
      okText: 'Trigger Portfolio Update',
      cancelText: 'Cancel',
      okButtonProps: { type: 'primary' },
      onOk: async () => {
        setLoading(true);
        setError(null);
        setSuccess(null);
        try {
          const response = await authRequest<{
            status: string;
            message: string;
            portfolio_cards: number;
          }>('post', '/card-updates/trigger-portfolio', {});
          setSuccess(
            `Portfolio update started for ${response.portfolio_cards} cards.`
          );
          await fetchStatus();
        } catch (triggerError: any) {
          setError(triggerError.message);
        } finally {
          setLoading(false);
        }
      },
    });
  };

  const handleTriggerCard = async (values: TriggerCardPayload) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const response = await authRequest<{
        card_name?: string;
        suggestions_created?: number;
        message?: string;
      }>(
        'post',
        `/card-updates/trigger-card/${values.cardId}`,
        {}
      );
      const suggestions = response.suggestions_created ?? 0;
      const baseMessage =
        response.message ||
        `Update completed for ${response.card_name || `card #${values.cardId}`}.`;
      const suffix =
        suggestions > 0
          ? ` ${suggestions} suggestion${suggestions === 1 ? '' : 's'} ready for review.`
          : ' No new suggestions detected.';
      setSuccess(`${baseMessage}${suffix}`);
      setShowCardModal(false);
      cardForm.resetFields();
      await fetchStatus();
    } catch (cardError: any) {
      setError(cardError.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTestExtraction = async (values: ExtractionPayload) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const data = await authRequest<{
        content_length: number;
        extracted_data?: Record<string, unknown>;
      }>('post', '/card-updates/extract-from-url', {
        url: values.url,
        card_name: values.cardName,
        bank_name: values.bankName,
        card_variant: values.cardVariant,
      });

      Modal.success({
        title: 'Extraction Successful',
        width: 640,
        content: (
          <div>
            <p>
              <strong>Content Length:</strong> {data.content_length}
            </p>
            <p>
              <strong>Detected Keys:</strong>{' '}
              {Object.keys(data.extracted_data || {}).join(', ') || 'None'}
            </p>
          </div>
        ),
      });

      extractForm.resetFields();
      setShowExtractModal(false);
      setSuccess('Extraction completed successfully.');
    } catch (extractError: any) {
      setError(extractError.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!success) return;
    const timer = window.setTimeout(() => setSuccess(null), 6000);
    return () => window.clearTimeout(timer);
  }, [success]);

  useEffect(() => {
    if (!error) return;
    const timer = window.setTimeout(() => setError(null), 6000);
    return () => window.clearTimeout(timer);
  }, [error]);

  return (
    <div className="px-6 py-8 space-y-16">
      <Card
        title={
          <Space size={12}>
            <ThunderboltOutlined />
            <span>Automated Card Updates</span>
          </Space>
        }
        extra={
          <Space>
            <Button
              icon={<ReloadOutlined />}
              onClick={fetchStatus}
              loading={fetching}
            >
              Refresh
            </Button>
            <Button
              type="default"
              icon={<ThunderboltOutlined />}
              onClick={handleTriggerPortfolio}
              loading={loading}
              style={{ borderColor: '#1890ff', color: '#1890ff' }}
            >
              Update Portfolio Cards
            </Button>
            <Button
              type="primary"
              icon={<ThunderboltOutlined />}
              onClick={handleTriggerAll}
              loading={loading}
              danger
            >
              Update All Cards
            </Button>
          </Space>
        }
        variant="borderless"
        style={{ boxShadow: '0 10px 25px rgba(15, 23, 42, 0.08)' }}
      >
        <Space direction="vertical" size={16} style={{ width: '100%' }}>
          {error && (
            <Alert
              type="error"
              message="Action failed"
              description={error}
              showIcon
              closable
              onClose={() => setError(null)}
            />
          )}
          {success && (
            <Alert
              type="success"
              message="Success"
              description={success}
              showIcon
              closable
              onClose={() => setSuccess(null)}
            />
          )}

          <Card
            size="small"
            title={
              <Space>
                <ClockCircleOutlined />
                <span>Status</span>
              </Space>
            }
            extra={
              status ? (
                status.is_running ? (
                  <Tag color="orange" icon={<ClockCircleOutlined />}>
                    Running
                  </Tag>
                ) : (
                  <Tag color="green" icon={<CheckCircleOutlined />}>
                    Idle
                  </Tag>
                )
              ) : null
            }
          >
            <Spin spinning={fetching}>
              <div className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide">
                      Scheduler
                    </p>
                    <p className="text-base text-gray-900">
                      {status?.scheduler_running ? 'Active' : 'Stopped'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide">
                      Next Run
                    </p>
                    <p className="text-base text-gray-900">
                      {formattedDate(status?.next_run)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide">
                      Processed (this run)
                    </p>
                    <p className="text-base text-gray-900">
                      {status?.is_running
                        ? `${processedCards} / ${totalCards || 'N/A'}`
                        : 'Idle'}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wide">
                      Suggestions (last summary)
                    </p>
                    <p className="text-base text-gray-900">
                      {status?.last_run_summary
                        ? status.last_run_summary.suggestions_created
                        : 'Not available'}
                    </p>
                  </div>
                </div>

                {status?.last_error && (
                  <Alert
                    type="warning"
                    message="Last run encountered an issue"
                    description={status.last_error}
                    showIcon
                  />
                )}

                {progress && totalCards > 0 && (
                  <div className="space-y-3">
                    <Progress
                      percent={progressPercent}
                      status={status?.is_running ? 'active' : 'normal'}
                    />
                    {currentCard && (
                      <Alert
                        type="info"
                        showIcon
                        message={`Checking ${currentCard.bank_name} ${currentCard.card_name}`}
                        description={
                          <Space direction="vertical" size={4}>
                            <span>
                              Stage:{' '}
                              <Tag color="blue">{stageLabel(currentCard.stage)}</Tag>
                            </span>
                            {currentCard.source_url && (
                              <a
                                href={currentCard.source_url}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                View official source
                              </a>
                            )}
                          </Space>
                        }
                      />
                    )}
                    {lastCompleted && (
                      <Alert
                        type="success"
                        showIcon
                        message={`Last processed: ${lastCompleted.bank_name} ${lastCompleted.card_name}`}
                        description={
                          <Space direction="vertical" size={2}>
                            <span>
                              Outcome:{' '}
                              <Tag color={lastCompleted.suggestions_created > 0 ? 'green' : 'default'}>
                                {stageLabel(lastCompleted.status)}
                              </Tag>
                            </span>
                            <span>
                              Suggestions created: {lastCompleted.suggestions_created}
                            </span>
                            <span>Completed at: {formattedDate(lastCompleted.timestamp)}</span>
                          </Space>
                        }
                      />
                    )}
                  </div>
                )}

                {status?.last_run_summary && (
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wide">
                        Last Completed
                      </p>
                      <p className="text-base text-gray-900">
                        {formattedDate(status.last_run_summary.completed_at)}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wide">
                        Processed Cards (last run)
                      </p>
                      <p className="text-base text-gray-900">
                        {status.last_run_summary.processed_cards} /{' '}
                        {status.last_run_summary.total_cards}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wide">
                        Skipped
                      </p>
                      <p className="text-base text-gray-900">
                        {status.last_run_summary.skipped}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wide">
                        Failed
                      </p>
                      <p className="text-base text-gray-900">
                        {status.last_run_summary.failed}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </Spin>
          </Card>

          <Card
            size="small"
            title={
              <Space>
                <ExperimentOutlined />
                <span>Manual Tools</span>
              </Space>
            }
            extra={
              <Space>
                <Button onClick={() => setShowCardModal(true)} disabled={loading}>
                  Trigger One Card
                </Button>
                <Button onClick={() => setShowExtractModal(true)} disabled={loading}>
                  Test Extraction
                </Button>
              </Space>
            }
          >
            <p className="text-gray-600">
              Use these tools to update a specific card or validate extraction
              from a bank URL. All actions require valid admin authentication.
            </p>
          </Card>
        </Space>
      </Card>

      <Modal
        title="Trigger Single Card Update"
        open={showCardModal}
        onCancel={() => {
          setShowCardModal(false);
          cardForm.resetFields();
        }}
        footer={null}
        destroyOnHidden
      >
        <Form<TriggerCardPayload>
          form={cardForm}
          layout="vertical"
          onFinish={handleTriggerCard}
        >
          <Form.Item
            label="Card ID"
            name="cardId"
            rules={[
              { required: true, message: 'Please enter a card ID' },
              {
                pattern: /^[0-9]+$/,
                message: 'Card ID must be a positive integer',
              },
            ]}
          >
            <Input placeholder="Enter the card ID (e.g., 123)" inputMode="numeric" />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button onClick={() => setShowCardModal(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit" loading={loading}>
                Trigger Update
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Test Extraction From URL"
        open={showExtractModal}
        onCancel={() => {
          setShowExtractModal(false);
          extractForm.resetFields();
        }}
        footer={null}
        width={560}
        destroyOnHidden
      >
        <Form<ExtractionPayload>
          form={extractForm}
          layout="vertical"
          onFinish={handleTestExtraction}
          initialValues={{ cardVariant: undefined }}
        >
          <Form.Item
            label="Bank URL"
            name="url"
            rules={[
              { required: true, message: 'Please enter the terms page URL' },
              {
                type: 'url',
                warningOnly: true,
                message: 'Please enter a valid URL including protocol',
              },
            ]}
          >
            <Input placeholder="https://www.bank.com/cards/hdfc-regalia" />
          </Form.Item>
          <Form.Item
            label="Card Name"
            name="cardName"
            rules={[{ required: true, message: 'Please enter the card name' }]}
          >
            <Input placeholder="Regalia Credit Card" />
          </Form.Item>
          <Form.Item
            label="Bank Name"
            name="bankName"
            rules={[{ required: true, message: 'Please enter the bank name' }]}
          >
            <Input placeholder="HDFC Bank" />
          </Form.Item>
          <Form.Item label="Card Variant (optional)" name="cardVariant">
            <Input placeholder="e.g., Visa Signature" />
          </Form.Item>
          <Form.Item>
            <Space>
              <Button onClick={() => setShowExtractModal(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit" loading={loading}>
                Run Extraction
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CardUpdateAdmin;
