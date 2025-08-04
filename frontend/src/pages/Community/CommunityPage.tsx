import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Plus, ArrowLeft, MessageSquare } from 'lucide-react';
import { communityAPI, cardMasterDataAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import PostCard from '../../components/Community/PostCard';
import LoadingSpinner from '../../components/UI/LoadingSpinner';

interface Post {
  id: number;
  title: string;
  body?: string;
  user_name: string;
  card_master_id: number;
  upvotes: number;
  downvotes: number;
  net_votes: number;
  comment_count: number;
  created_at: string;
  updated_at: string;
}

interface CardData {
  id: number;
  display_name: string;
  bank_name: string;
  card_name: string;
}

const CommunityPage: React.FC = () => {
  const { cardId } = useParams<{ cardId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [posts, setPosts] = useState<Post[]>([]);
  const [cardData, setCardData] = useState<CardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'votes'>('newest');
  const [totalCount, setTotalCount] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  // Form state
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const loadCardData = async () => {
    try {
      const response = await cardMasterDataAPI.getCardById(cardId!);
      setCardData(response);
    } catch (error) {
      console.error('Error loading card data:', error);
      navigate('/all-cards');
    }
  };

  const loadPosts = async (reset = false) => {
    try {
      const skip = reset ? 0 : currentPage * 10;
      const response = await communityAPI.getCardPosts(cardId!, {
        skip,
        limit: 10,
        sort_by: sortBy
      });
      
      if (reset) {
        setPosts(response.posts);
        setCurrentPage(0);
      } else {
        setPosts(prev => [...prev, ...response.posts]);
      }
      
      setTotalCount(response.total_count);
      setHasMore(response.posts.length === 10);
    } catch (error) {
      console.error('Error loading posts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (cardId) {
      loadCardData();
      loadPosts(true);
    }
  }, [cardId, sortBy]);

  const handleCreatePost = async () => {
    if (!user || !title.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.createPost(cardId!, {
        title: title.trim(),
        body: body.trim() || undefined
      });
      
      setTitle('');
      setBody('');
      setShowCreateForm(false);
      loadPosts(true);
    } catch (error) {
      console.error('Error creating post:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      setCurrentPage(prev => prev + 1);
      loadPosts();
    }
  };

  const handleVoteChange = () => {
    loadPosts(true);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!cardData) {
    return <div className="text-center py-8">Card not found</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate(`/cards/${cardId}`)}
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Card Details</span>
          </button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                Community Discussion
              </h1>
              <p className="text-gray-600 dark:text-gray-300">
                {cardData.display_name} • {cardData.bank_name}
              </p>
            </div>
            
            {user && (
              <button
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>New Post</span>
              </button>
            )}
          </div>
        </div>

        {/* Create Post Form */}
        {showCreateForm && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Create New Post
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Title *
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  placeholder="Enter post title..."
                  maxLength={300}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Body (Optional)
                </label>
                <textarea
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  rows={4}
                  placeholder="Enter post content..."
                />
              </div>
              
              <div className="flex space-x-3">
                <button
                  onClick={handleCreatePost}
                  disabled={isSubmitting || !title.trim()}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50"
                >
                  {isSubmitting ? 'Creating...' : 'Create Post'}
                </button>
                <button
                  onClick={() => {
                    setShowCreateForm(false);
                    setTitle('');
                    setBody('');
                  }}
                  className="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Sort Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Sort by:
              </span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'newest' | 'oldest' | 'votes')}
                className="p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="newest">Newest</option>
                <option value="oldest">Oldest</option>
                <option value="votes">Most Voted</option>
              </select>
            </div>
            
            <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
              <MessageSquare className="w-4 h-4" />
              <span>{totalCount} posts</span>
            </div>
          </div>
        </div>

        {/* Posts List */}
        <div className="space-y-4">
          {posts.length > 0 ? (
            posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                onVoteChange={handleVoteChange}
              />
            ))
          ) : (
            <div className="text-center py-12">
              <MessageSquare className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                No posts yet
              </h3>
              <p className="text-gray-500 dark:text-gray-400 mb-4">
                Be the first to start a discussion about this card!
              </p>
              {user && (
                <button
                  onClick={() => setShowCreateForm(true)}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
                >
                  Create First Post
                </button>
              )}
            </div>
          )}
        </div>

        {/* Load More Button */}
        {hasMore && posts.length > 0 && (
          <div className="text-center mt-6">
            <button
              onClick={handleLoadMore}
              disabled={loading}
              className="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Load More Posts'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default CommunityPage; 