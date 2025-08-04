import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ThumbsUp, ThumbsDown, MessageSquare, User, Clock, Edit, Trash2 } from 'lucide-react';
import { communityAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import CommentComponent from '../../components/Community/Comment';
import LoadingSpinner from '../../components/UI/LoadingSpinner';
import { formatTimeAgo } from '../../utils/timeUtils';

interface CommentData {
  id: number;
  body: string;
  user_name: string;
  user_id: number;
  upvotes: number;
  downvotes: number;
  net_votes: number;
  created_at: string;
  updated_at: string;
  replies: CommentData[];
}

interface Post {
  id: number;
  title: string;
  body?: string;
  user_name: string;
  user_id: number;
  card_master_id: number;
  upvotes: number;
  downvotes: number;
  net_votes: number;
  comment_count: number;
  created_at: string;
  updated_at: string;
  comments: CommentData[];
}

const PostDetailPage: React.FC = () => {
  const { postId } = useParams<{ postId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [isVoting, setIsVoting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editBody, setEditBody] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [newComment, setNewComment] = useState('');

  const loadPost = async () => {
    try {
      const response = await communityAPI.getPostDetail(postId!);
      setPost(response);
      setEditTitle(response.title);
      setEditBody(response.body || '');
    } catch (error) {
      console.error('Error loading post:', error);
      navigate('/all-cards');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (postId) {
      loadPost();
    }
  }, [postId]);

  const handleVote = async (voteType: 'upvote' | 'downvote') => {
    if (!user || isVoting) return;
    
    setIsVoting(true);
    try {
      await communityAPI.voteOnPost(postId!, voteType);
      loadPost();
    } catch (error) {
      console.error('Error voting on post:', error);
    } finally {
      setIsVoting(false);
    }
  };

  const handleEdit = async () => {
    if (!user || !editTitle.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.updatePost(postId!, {
        title: editTitle.trim(),
        body: editBody.trim() || undefined
      });
      setIsEditing(false);
      loadPost();
    } catch (error) {
      console.error('Error updating post:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!user || isSubmitting) return;
    
    if (!window.confirm('Are you sure you want to delete this post?')) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.deletePost(postId!);
      navigate(`/community/${post?.card_master_id}`);
    } catch (error) {
      console.error('Error deleting post:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCreateComment = async () => {
    if (!user || !newComment.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.createComment(postId!, {
        body: newComment.trim()
      });
      setNewComment('');
      loadPost();
    } catch (error) {
      console.error('Error creating comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const canEdit = user && post && user.id === post.user_id;

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!post) {
    return <div className="text-center py-8">Post not found</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate(`/community/${post.card_master_id}`)}
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Community</span>
          </button>
        </div>

        {/* Post Content */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
          <div className="flex items-start space-x-3">
            {/* Vote buttons */}
            <div className="flex flex-col items-center space-y-1">
              <button
                onClick={() => handleVote('upvote')}
                disabled={isVoting}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <ThumbsUp className={`w-4 h-4 ${
                  post.net_votes > 0 ? 'text-green-500' : 'text-gray-400'
                }`} />
              </button>
              
              <span className="text-sm font-medium text-gray-900 dark:text-white">
                {post.net_votes}
              </span>
              
              <button
                onClick={() => handleVote('downvote')}
                disabled={isVoting}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <ThumbsDown className={`w-4 h-4 ${
                  post.net_votes < 0 ? 'text-red-500' : 'text-gray-400'
                }`} />
              </button>
            </div>

            {/* Post content */}
            <div className="flex-1 min-w-0">
              {isEditing ? (
                <div className="space-y-4">
                  <input
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-xl font-semibold"
                    maxLength={300}
                  />
                  <textarea
                    value={editBody}
                    onChange={(e) => setEditBody(e.target.value)}
                    className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    rows={6}
                  />
                  <div className="flex space-x-3">
                    <button
                      onClick={handleEdit}
                      disabled={isSubmitting}
                      className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50"
                    >
                      Save Changes
                    </button>
                    <button
                      onClick={() => {
                        setIsEditing(false);
                        setEditTitle(post.title);
                        setEditBody(post.body || '');
                      }}
                      className="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {post.title}
                    </h1>
                    
                    {canEdit && (
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => setIsEditing(true)}
                          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                        >
                          <Edit className="w-4 h-4 text-gray-500" />
                        </button>
                        <button
                          onClick={handleDelete}
                          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </button>
                      </div>
                    )}
                  </div>
                  
                  {post.body && (
                    <p className="text-gray-700 dark:text-gray-300 mb-4 text-lg">
                      {post.body}
                    </p>
                  )}
                </div>
              )}

              {/* Post metadata */}
              <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-1">
                    <User className="w-4 h-4" />
                    <span>{post.user_name}</span>
                  </div>
                  
                  <div className="flex items-center space-x-1">
                    <Clock className="w-4 h-4" />
                    <span>{formatTimeAgo(post.created_at)}</span>
                  </div>
                </div>

                <div className="flex items-center space-x-1">
                  <MessageSquare className="w-4 h-4" />
                  <span>{post.comment_count} comments</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* New Comment Form */}
        {user && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Add a Comment
            </h3>
            
            <div className="space-y-4">
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                rows={4}
                placeholder="Write your comment..."
              />
              
              <div className="flex justify-end">
                <button
                  onClick={handleCreateComment}
                  disabled={isSubmitting || !newComment.trim()}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50"
                >
                  {isSubmitting ? 'Posting...' : 'Post Comment'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Comments Section */}
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
            Comments ({post.comment_count})
          </h3>
          
          {post.comments.length > 0 ? (
            post.comments.map((comment) => (
              <CommentComponent
                key={comment.id}
                comment={comment}
                postId={post.id}
                onVoteChange={loadPost}
                onCommentChange={loadPost}
              />
            ))
          ) : (
            <div className="text-center py-8">
              <MessageSquare className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
              <p className="text-gray-500 dark:text-gray-400">
                No comments yet. Be the first to comment!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PostDetailPage; 