import React from 'react';
import '@testing-library/jest-dom';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { act } from 'react-dom/test-utils';
import AdminDashboardPage, { SUGGESTIONS_PAGE_SIZE } from '../AdminDashboardPage';
import { adminAPI } from '../../../services/api';
import { useAuth } from '../../../hooks/useAuth';

jest.mock('../../../services/api', () => ({
  adminAPI: {
    getStats: jest.fn(),
    getUsers: jest.fn(),
    getModeratorRequests: jest.fn(),
    getEditSuggestions: jest.fn(),
    getCardDocuments: jest.fn(),
    reviewEditSuggestion: jest.fn(),
    reviewModeratorRequest: jest.fn(),
    reviewCardDocument: jest.fn(),
    getChatAccessRequests: jest.fn(),
    getChatAccessStats: jest.fn(),
    reviewChatAccessRequest: jest.fn(),
  },
}));
jest.mock('../../../hooks/useAuth');
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));

jest.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...rest }: any) => <div {...rest}>{children}</div>,
  },
}));

const createSuggestion = (id: number, status: 'pending' | 'approved' | 'rejected', createdDate: string) => ({
  id,
  field_type: 'spending_category',
  field_name: `category_${id}`,
  old_value: '1',
  new_value: '2',
  status,
  created_at: createdDate,
  user_name: `User ${id}`,
  card_name: `Card ${id}`,
  bank_name: `Bank ${id}`,
  suggestion_reason: 'Automated update',
});

describe('AdminDashboardPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    (useAuth as jest.Mock).mockReturnValue({
      user: { email: 'ashokkalbhor@gmail.com' },
    });

    (adminAPI.getStats as jest.Mock).mockResolvedValue({
      users: { total: 1, active: 1, moderators: 0 },
      moderator_requests: { pending: 0 },
      edit_suggestions: { pending: SUGGESTIONS_PAGE_SIZE + 5, approved: 0, rejected: 0 },
      card_documents: { pending: 0, approved: 0, rejected: 0 },
      recent_activity: [],
    });
    (adminAPI.getUsers as jest.Mock).mockResolvedValue([]);
    (adminAPI.getModeratorRequests as jest.Mock).mockResolvedValue([]);
    (adminAPI.getCardDocuments as jest.Mock).mockResolvedValue([]);
    (adminAPI.reviewEditSuggestion as jest.Mock).mockResolvedValue(undefined);
  });

  it('loads additional edit suggestion pages when requested', async () => {
    const baseDate = new Date('2025-01-01T12:00:00Z').getTime();
    const firstPage = [
      createSuggestion(1, 'pending', new Date(baseDate + 3).toISOString()),
      createSuggestion(2, 'approved', new Date(baseDate + 4).toISOString()),
      ...Array.from({ length: SUGGESTIONS_PAGE_SIZE - 2 }, (_, index) =>
        createSuggestion(
          index + 3,
          'pending',
          new Date(baseDate - (index + 3)).toISOString()
        )
      ),
    ];
    const secondPage = [
      createSuggestion(SUGGESTIONS_PAGE_SIZE + 1, 'pending', new Date(baseDate + 2).toISOString()),
      createSuggestion(SUGGESTIONS_PAGE_SIZE + 2, 'rejected', new Date(baseDate + 1).toISOString()),
      ...Array.from({ length: 3 }, (_, index) =>
        createSuggestion(
          SUGGESTIONS_PAGE_SIZE + 3 + index,
          'pending',
          new Date(baseDate - (index + 10)).toISOString()
        )
      ),
    ];

    (adminAPI.getEditSuggestions as jest.Mock)
      .mockResolvedValueOnce(firstPage)
      .mockResolvedValueOnce(secondPage);

    render(<AdminDashboardPage />);

    const suggestionsTab = await screen.findByRole('button', { name: /edit suggestions/i });
    await act(async () => {
      await userEvent.click(suggestionsTab);
    });

    await waitFor(() => expect(screen.getByText('Card 1')).toBeInTheDocument());

    expect(adminAPI.getEditSuggestions).toHaveBeenCalledWith({
      skip: 0,
      limit: SUGGESTIONS_PAGE_SIZE,
    });

    const loadMoreButton = await screen.findByRole('button', { name: /load more suggestions/i });

    await act(async () => {
      await userEvent.click(loadMoreButton);
    });

    await waitFor(() =>
      expect(screen.getByText(`Card ${SUGGESTIONS_PAGE_SIZE + 1}`)).toBeInTheDocument()
    );

    expect(adminAPI.getEditSuggestions).toHaveBeenLastCalledWith({
      skip: SUGGESTIONS_PAGE_SIZE,
      limit: SUGGESTIONS_PAGE_SIZE,
    });

    expect(screen.queryByRole('button', { name: /load more suggestions/i })).not.toBeInTheDocument();

    const headingTexts = screen
      .getAllByRole('heading', { level: 3 })
      .map((heading) => heading.textContent);

    const indexCard1 = headingTexts.indexOf('Card 1');
    const indexCard26 = headingTexts.indexOf(`Card ${SUGGESTIONS_PAGE_SIZE + 1}`);
    const indexCard2 = headingTexts.indexOf('Card 2');
    const indexCard27 = headingTexts.indexOf(`Card ${SUGGESTIONS_PAGE_SIZE + 2}`);

    expect(indexCard1).toBeGreaterThan(-1);
    expect(indexCard26).toBeGreaterThan(-1);
    expect(indexCard2).toBeGreaterThan(-1);
    expect(indexCard27).toBeGreaterThan(-1);

    expect(indexCard1).toBeLessThan(indexCard2);
    expect(indexCard26).toBeLessThan(indexCard2);
    expect(indexCard2).toBeLessThan(indexCard27);
  });

  it('bulk approves all currently loaded pending suggestions', async () => {
    const baseDate = new Date('2025-02-01T00:00:00Z').getTime();
    const initialSuggestions = [
      createSuggestion(101, 'pending', new Date(baseDate).toISOString()),
      createSuggestion(102, 'pending', new Date(baseDate - 1000).toISOString()),
      createSuggestion(103, 'approved', new Date(baseDate - 2000).toISOString()),
    ];
    const refreshedSuggestions = [
      { ...initialSuggestions[0], status: 'approved' as const },
      { ...initialSuggestions[1], status: 'approved' as const },
      initialSuggestions[2],
    ];

    (adminAPI.getEditSuggestions as jest.Mock)
      .mockResolvedValueOnce(initialSuggestions)
      .mockResolvedValueOnce(refreshedSuggestions);

    render(<AdminDashboardPage />);

    const suggestionsTab = await screen.findByRole('button', { name: /edit suggestions/i });
    await act(async () => {
      await userEvent.click(suggestionsTab);
    });

    await waitFor(() => expect(screen.getByText('Card 101')).toBeInTheDocument());

    const approveAllButton = screen.getByRole('button', { name: /approve all pending/i });
    expect(approveAllButton).not.toBeDisabled();

    await act(async () => {
      await userEvent.click(approveAllButton);
    });

    await waitFor(() => expect(adminAPI.reviewEditSuggestion).toHaveBeenCalledTimes(2));
    expect(adminAPI.reviewEditSuggestion).toHaveBeenNthCalledWith(1, 101, {
      status: 'approved',
      review_notes: undefined,
    });
    expect(adminAPI.reviewEditSuggestion).toHaveBeenNthCalledWith(2, 102, {
      status: 'approved',
      review_notes: undefined,
    });

    await waitFor(() => expect(adminAPI.getEditSuggestions).toHaveBeenCalledTimes(2));

    await waitFor(() =>
      expect(screen.getByRole('button', { name: /approve all pending/i })).toBeDisabled()
    );
  });
});
