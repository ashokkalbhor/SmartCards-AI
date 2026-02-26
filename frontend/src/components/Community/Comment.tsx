import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, Reply, Edit, Trash2, User } from 'lucide-react';
import { communityAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
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

interface CommentProps {
  comment: CommentData;
  postId: number;
  onVoteChange?: () => void;
  onCommentChange?: () => void;
  depth?: number;
}

const Comment: React.FC<CommentProps> = ({ 
  comment, 
  postId, 
  onVoteChange, 
  onCommentChange,
  depth = 0 
}) => {
  const { user } = useAuth();
  const [isVoting, setIsVoting] = useState(false);
  const [isReplying, setIsReplying] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [replyText, setReplyText] = useState('');
  const [editText, setEditText] = useState(comment.body);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleVote = async (voteType: 'upvote' | 'downvote') => {
    if (!user || isVoting) return;
    
    setIsVoting(true);
    try {
      await communityAPI.voteOnComment(comment.id.toString(), voteType);
      onVoteChange?.();
    } catch (error) {
      console.error('Error voting on comment:', error);
    } finally {
      setIsVoting(false);
    }
  };

  const handleReply = async () => {
    if (!user || !replyText.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.createComment(postId.toString(), {
        body: replyText,
        parent_id: comment.id
      });
      setReplyText('');
      setIsReplying(false);
      onCommentChange?.();
    } catch (error) {
      console.error('Error creating reply:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEdit = async () => {
    if (!user || !editText.trim() || isSubmitting) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.updateComment(comment.id.toString(), {
        body: editText
      });
      setIsEditing(false);
      onCommentChange?.();
    } catch (error) {
      console.error('Error updating comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!user || isSubmitting) return;
    
    if (!window.confirm('Are you sure you want to delete this comment?')) return;
    
    setIsSubmitting(true);
    try {
      await communityAPI.deleteComment(comment.id.toString());
      onCommentChange?.();
    } catch (error) {
      console.error('Error deleting comment:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const canEdit = user && user.id === comment.user_id;
  const maxDepth = 3; // Limit nesting depth

  return (
    <div className={`${depth > 0 ? 'ml-6 border-l-2 border-gray-200 dark:border-gray-700 pl-4' : ''}`}>
      <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3 mb-3">
        {/* Comment header */}
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-2">
            <User className="w-4 h-4 text-gray-500" />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              {comment.user_name}
            </span>
            <span className="text-xs text-gray-500">
              {formatTimeAgo(comment.created_at)}
            </span>
          </div>
          
          {canEdit && (
            <div className="flex items-center space-x-1">
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
              >
                <Edit className="w-3 h-3 text-gray-500" />
              </button>
              <button
                onClick={handleDelete}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
              >
                <Trash2 className="w-3 h-3 text-red-500" />
              </button>
            </div>
          )}
        </div>

        {/* Comment content */}
        {isEditing ? (
          <div className="mb-3">
            <textarea
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              rows={3}
            />
            <div className="flex space-x-2 mt-2">
              <button
                onClick={handleEdit}
                disabled={isSubmitting}
                className="px-3 py-1 bg-primary-600 text-white rounded text-sm hover:bg-primary-700 disabled:opacity-50"
              >
                Save
              </button>
              <button
                onClick={() => {
                  setIsEditing(false);
                  setEditText(comment.body);
                }}
                className="px-3 py-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded text-sm hover:bg-gray-400 dark:hover:bg-gray-500"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <p className="text-gray-700 dark:text-gray-300 mb-3">
            {comment.body}
          </p>
        )}

        {/* Comment actions */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {/* Vote buttons */}
            <div className="flex items-center space-x-1">
              <button
                onClick={() => handleVote('upvote')}
                disabled={isVoting}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
              >
                <ThumbsUp className={`w-3 h-3 ${
                  comment.net_votes > 0 ? 'text-green-500' : 'text-gray-400'
                }`} />
              </button>
              
              <span className="text-xs font-medium text-gray-900 dark:text-white">
                {comment.net_votes}
              </span>
              
              <button
                onClick={() => handleVote('downvote')}
                disabled={isVoting}
                className="p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded transition-colors"
              >
                <ThumbsDown className={`w-3 h-3 ${
                  comment.net_votes < 0 ? 'text-red-500' : 'text-gray-400'
                }`} />
              </button>
            </div>

            {/* Reply button */}
            {depth < maxDepth && user && (
              <button
                onClick={() => setIsReplying(!isReplying)}
                className="flex items-center space-x-1 text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
              >
                <Reply className="w-3 h-3" />
                <span>Reply</span>
              </button>
            )}
          </div>
        </div>

        {/* Reply form */}
        {isReplying && (
          <div className="mt-3">
            <textarea
              value={replyText}
              onChange={(e) => setReplyText(e.target.value)}
              placeholder="Write a reply..."
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              rows={3}
            />
            <div className="flex space-x-2 mt-2">
              <button
                onClick={handleReply}
                disabled={isSubmitting || !replyText.trim()}
                className="px-3 py-1 bg-primary-600 text-white rounded text-sm hover:bg-primary-700 disabled:opacity-50"
              >
                Reply
              </button>
              <button
                onClick={() => {
                  setIsReplying(false);
                  setReplyText('');
                }}
                className="px-3 py-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded text-sm hover:bg-gray-400 dark:hover:bg-gray-500"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Nested replies */}
      {comment.replies && comment.replies.length > 0 && depth < maxDepth && (
        <div className="space-y-2">
          {comment.replies.map((reply) => (
            <Comment
              key={reply.id}
              comment={reply}
              postId={postId}
              onVoteChange={onVoteChange}
              onCommentChange={onCommentChange}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Comment; 