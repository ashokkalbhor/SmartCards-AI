import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ThumbsUp, ThumbsDown, MessageSquare, User, Clock } from 'lucide-react';
import { communityAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import { formatTimeAgo } from '../../utils/timeUtils';

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

interface PostCardProps {
  post: Post;
  onVoteChange?: () => void;
}

const PostCard: React.FC<PostCardProps> = ({ post, onVoteChange }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [isVoting, setIsVoting] = useState(false);

  const handleVote = async (voteType: 'upvote' | 'downvote') => {
    if (!user || isVoting) return;
    
    setIsVoting(true);
    try {
      await communityAPI.voteOnPost(post.id.toString(), voteType);
      onVoteChange?.();
    } catch (error) {
      console.error('Error voting on post:', error);
    } finally {
      setIsVoting(false);
    }
  };

  const handlePostClick = () => {
    navigate(`/community/post/${post.id}`);
  };

  return (
    <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
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
          <div 
            className="cursor-pointer"
            onClick={handlePostClick}
          >
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
              {post.title}
            </h3>
            
            {post.body && (
              <p className="text-gray-600 dark:text-gray-300 mb-3 line-clamp-3">
                {post.body}
              </p>
            )}
          </div>

          {/* Post metadata */}
          <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
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
  );
};

export default PostCard; 