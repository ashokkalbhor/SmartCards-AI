import React from 'react';
import { Star, ThumbsUp, ThumbsDown, User, CheckCircle } from 'lucide-react';

interface Review {
  id: number;
  user_id: number;
  card_master_id: number;
  user_name: string;
  overall_rating: number;
  review_title?: string;
  review_content?: string;
  pros?: string;
  cons?: string;
  experience?: string;
  is_verified_cardholder: boolean;
  helpful_votes: number;
  created_at: string;
  updated_at: string;
}

interface ReviewListProps {
  reviews: Review[];
  onVote: (reviewId: string, voteType: 'helpful' | 'not_helpful') => void;
  currentUserId?: number;
}

const ReviewList: React.FC<ReviewListProps> = ({ reviews, onVote, currentUserId }) => {
  const renderStars = (rating: number) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <Star
          key={i}
          className={`w-4 h-4 ${
            i <= rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
          }`}
        />
      );
    }
    return stars;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (reviews.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-500 text-lg mb-2">No reviews yet</div>
        <div className="text-gray-400 text-sm">
          Be the first to share your experience with this card!
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {reviews.map((review) => (
        <div key={review.id} className="bg-gray-50 rounded-lg p-6">
          {/* Review Header */}
          <div className="flex justify-between items-start mb-4">
            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <User className="w-5 h-5 text-gray-400" />
                <span className="font-medium text-gray-900">{review.user_name}</span>
                {review.is_verified_cardholder && (
                  <CheckCircle className="w-4 h-4 text-green-500" />
                )}
              </div>
              <span className="text-gray-400">•</span>
              <span className="text-sm text-gray-500">{formatDate(review.created_at)}</span>
            </div>
            <div className="flex items-center space-x-1">
              {renderStars(review.overall_rating)}
            </div>
          </div>

          {/* Review Title */}
          {review.review_title && (
            <h4 className="font-semibold text-gray-900 mb-2">{review.review_title}</h4>
          )}

          {/* Review Content */}
          {review.review_content && (
            <p className="text-gray-700 mb-4 leading-relaxed">{review.review_content}</p>
          )}

          {/* Pros and Cons */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            {review.pros && (
              <div className="bg-green-50 p-3 rounded-lg">
                <h5 className="font-medium text-green-800 mb-1">Pros</h5>
                <p className="text-green-700 text-sm">{review.pros}</p>
              </div>
            )}
            {review.cons && (
              <div className="bg-red-50 p-3 rounded-lg">
                <h5 className="font-medium text-red-800 mb-1">Cons</h5>
                <p className="text-red-700 text-sm">{review.cons}</p>
              </div>
            )}
          </div>

          {/* Experience */}
          {review.experience && (
            <div className="bg-blue-50 p-3 rounded-lg mb-4">
              <h5 className="font-medium text-blue-800 mb-1">Experience</h5>
              <p className="text-blue-700 text-sm">{review.experience}</p>
            </div>
          )}

          {/* Review Footer */}
          <div className="flex justify-between items-center pt-4 border-t border-gray-200">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => onVote(review.id.toString(), 'helpful')}
                className="flex items-center space-x-1 text-gray-500 hover:text-green-600 transition-colors"
                disabled={currentUserId === review.user_id}
              >
                <ThumbsUp className="w-4 h-4" />
                <span className="text-sm">Helpful</span>
              </button>
              <button
                onClick={() => onVote(review.id.toString(), 'not_helpful')}
                className="flex items-center space-x-1 text-gray-500 hover:text-red-600 transition-colors"
                disabled={currentUserId === review.user_id}
              >
                <ThumbsDown className="w-4 h-4" />
                <span className="text-sm">Not Helpful</span>
              </button>
              {review.helpful_votes > 0 && (
                <span className="text-sm text-gray-500">
                  {review.helpful_votes} found this helpful
                </span>
              )}
            </div>
            
            {review.updated_at !== review.created_at && (
              <span className="text-xs text-gray-400">
                Edited {formatDate(review.updated_at)}
              </span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ReviewList; 