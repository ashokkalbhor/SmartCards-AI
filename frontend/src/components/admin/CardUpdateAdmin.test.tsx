import '@testing-library/jest-dom';
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';

jest.mock('axios', () => {
  const request = jest.fn();
  return {
    __esModule: true,
    default: { request },
  };
});

const mockedAxios = require('axios').default as { request: jest.Mock };

const mockStatus = {
  is_running: false,
  scheduler_running: true,
  next_run: '2024-01-01T00:00:00Z',
  progress: {
    total_cards: 0,
    processed_cards: 0,
    current: null,
    last_completed: null,
  },
  last_run_summary: null,
  last_error: null,
};

type CardUpdateAdminComponent = typeof import('./CardUpdateAdmin').default;
let CardUpdateAdmin: CardUpdateAdminComponent;

describe('CardUpdateAdmin', () => {
  beforeAll(() => {
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: jest.fn().mockImplementation((query) => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      })),
    });
    CardUpdateAdmin = require('./CardUpdateAdmin').default;
  });

  beforeEach(() => {
    jest.useFakeTimers();
    localStorage.setItem('access_token', 'test-token');
    mockedAxios.request.mockImplementation(async (config) => {
      if (config.url?.endsWith('/card-updates/status')) {
        return { data: mockStatus } as any;
      }
      if (config.url?.includes('/card-updates/trigger-card/')) {
        return {
          data: {
            card_name: 'Sample Card',
            suggestions_created: 0,
            message: 'Update completed for Sample Card',
          },
        } as any;
      }
      if (config.url?.endsWith('/card-updates/trigger-all')) {
        return { data: { status: 'started' } } as any;
      }
      if (config.url?.endsWith('/card-updates/extract-from-url')) {
        return { data: { content_length: 123, extracted_data: {} } } as any;
      }
      return { data: {} } as any;
    });
  });

  afterEach(() => {
    act(() => { jest.runOnlyPendingTimers(); });
    jest.useRealTimers();
    mockedAxios.request.mockReset();
    localStorage.clear();
  });

  const renderAdmin = async () => {
    await act(async () => { render(<CardUpdateAdmin />); });
  };

  it('fetches and displays status information on mount', async () => {
    await renderAdmin();

    expect(await screen.findByText(/Automated Card Updates/i)).toBeInTheDocument();
    expect(await screen.findByText(/Scheduler/i)).toBeInTheDocument();
    expect(await screen.findByText(/Active/i)).toBeInTheDocument();
  });

  it('shows authentication error when no token is available', async () => {
    localStorage.removeItem('access_token');
    mockedAxios.request.mockClear();

    await renderAdmin();

    expect(await screen.findByText(/Authentication required/i)).toBeInTheDocument();
    expect(mockedAxios.request).not.toHaveBeenCalled();
  });

  it('submits single card update form successfully', async () => {
    await renderAdmin();

    fireEvent.click(await screen.findByRole('button', { name: /Trigger One Card/i }));
    const input = await screen.findByPlaceholderText(/e\.g\. 42/i);
    fireEvent.change(input, { target: { value: '123' } });
    fireEvent.click(screen.getByRole('button', { name: /Trigger Update/i }));

    await waitFor(() =>
      expect(screen.getByText(/Update completed for Sample Card/i)).toBeInTheDocument()
    );

    await act(async () => { jest.advanceTimersByTime(6000); });

    await waitFor(() =>
      expect(screen.queryByText(/Update completed for Sample Card/i)).not.toBeInTheDocument()
    );
  });
});
