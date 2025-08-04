import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { cardMasterDataAPI, cardReviewsAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import ReviewForm from '../../components/UI/ReviewForm';
import LoadingSpinner from '../../components/UI/LoadingSpinner';
import { ArrowLeft, CreditCard, Star, MessageSquare, ThumbsUp, ThumbsDown, User, CheckCircle, ChevronDown, ChevronUp } from 'lucide-react';

interface CardData {
  id: number;
  bank_name: string;
  card_name: string;
  card_variant?: string;
  display_name: string;
  card_network: string;
  card_tier: string;
  joining_fee?: number;
  annual_fee?: number;
  is_lifetime_free: boolean;
  joining_fee_display: string;
  annual_fee_display: string;
  description?: string;
  additional_features?: any;
  spending_categories?: Array<{
    id: number;
    category_name: string;
    category_display_name: string;
    reward_rate: number;
    reward_type: string;
    reward_display: string;
    is_active: boolean;
  }>;
  merchant_rewards?: Array<{
    id: number;
    merchant_name: string;
    merchant_display_name: string;
    reward_rate: number;
    reward_type: string;
    reward_display: string;
    is_active: boolean;
  }>;
}

interface ReviewData {
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

interface ReviewsResponse {
  reviews: ReviewData[];
  total_count: number;
  average_rating: number;
}

const CardDetailPage: React.FC = () => {
  const { cardId } = useParams<{ cardId: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [cardData, setCardData] = useState<CardData | null>(null);
  const [reviews, setReviews] = useState<ReviewsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [userReview, setUserReview] = useState<ReviewData | null>(null);
  const [showAllMerchants, setShowAllMerchants] = useState(false);
  const [showAllCategories, setShowAllCategories] = useState(false);

  const loadCardData = useCallback(async () => {
    try {
      // Use the specific card endpoint to get detailed data with spending categories and merchant rewards
      const response = await cardMasterDataAPI.getCardById(cardId!);
      if (response) {
        setCardData(response);
      } else {
        // Card not found, redirect to all-cards page
        navigate('/all-cards');
      }
    } catch (error) {
      console.error('Error loading card data:', error);
      navigate('/all-cards');
    }
  }, [cardId, navigate]);

  const loadReviews = useCallback(async () => {
    try {
      const response = await cardReviewsAPI.getCardReviews(cardId!);
      setReviews(response);
      
      // Check if current user has already reviewed this card
      if (user) {
        const userReview = response.reviews.find((r: ReviewData) => r.user_id === user.id);
        setUserReview(userReview || null);
      }
    } catch (error) {
      console.error('Error loading reviews:', error);
    } finally {
      setLoading(false);
    }
  }, [cardId, user]);

  useEffect(() => {
    if (cardId) {
      loadCardData();
      loadReviews();
    }
  }, [cardId, loadCardData, loadReviews]);

  const handleReviewSubmit = async (reviewData: any) => {
    try {
      if (userReview) {
        // Update existing review
        await cardReviewsAPI.updateReview(userReview.id.toString(), reviewData);
      } else {
        // Create new review - include card_master_id
        const reviewDataWithCardId = {
          ...reviewData,
          card_master_id: parseInt(cardId!)
        };
        await cardReviewsAPI.createReview(cardId!, reviewDataWithCardId);
      }
      
      // Reload reviews
      await loadReviews();
      setShowReviewForm(false);
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  };

  const handleReviewDelete = async () => {
    if (!userReview) return;
    
    try {
      await cardReviewsAPI.deleteReview(userReview.id.toString());
      setUserReview(null);
      await loadReviews();
    } catch (error) {
      console.error('Error deleting review:', error);
    }
  };

  const handleVote = async (reviewId: string, voteType: 'helpful' | 'not_helpful') => {
    try {
      await cardReviewsAPI.voteOnReview(reviewId, voteType);
      await loadReviews(); // Reload to get updated vote counts
    } catch (error) {
      console.error('Error voting on review:', error);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!cardData) {
    return <div className="text-center py-8">Card not found</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/all-cards')}
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to All Cards</span>
          </button>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">{cardData.display_name}</h1>
          <p className="text-gray-600 dark:text-gray-300">{cardData.description}</p>
        </div>

        {/* Main Content - Three Sections */}
        <div className="space-y-6">
          {/* Section 1: Card Details Table */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
                <CreditCard className="w-5 h-5 mr-2" />
                Card Details Table
              </h2>
            </div>
            
            <div className="p-6">
              {/* Basic Card Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Basic Information</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Bank:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{cardData.bank_name}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Network:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{cardData.card_network}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Tier:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{cardData.card_tier}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Joining Fee:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{cardData.joining_fee_display}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Annual Fee:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{cardData.annual_fee_display}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Reviews Summary</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Total Reviews:</span>
                      <span className="font-medium text-gray-900 dark:text-white">{reviews?.total_count || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-400">Average Rating:</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        {reviews?.average_rating ? `${reviews.average_rating.toFixed(1)}/5` : 'No reviews yet'}
                      </span>
                    </div>
                    <div className="flex items-center mt-2">
                      <span className="text-gray-600 dark:text-gray-400 mr-2">Rating:</span>
                      <div className="flex items-center">
                        {[1, 2, 3, 4, 5].map((star) => (
                          <Star
                            key={star}
                            className={`w-4 h-4 ${
                              star <= (reviews?.average_rating || 0)
                                ? 'text-yellow-400 fill-current'
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">Additional Features</h3>
                  <div className="space-y-2 text-sm">
                    {cardData.additional_features && typeof cardData.additional_features === 'object' ? (
                      Object.entries(cardData.additional_features).map(([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-gray-600 dark:text-gray-400 capitalize">
                            {key.replace(/_/g, ' ')}:
                          </span>
                          <span className="font-medium text-gray-900 dark:text-white">
                            {String(value)}
                          </span>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-500 dark:text-gray-400">No additional features listed</p>
                    )}
                  </div>
                </div>
              </div>

              {/* Spending Categories and Merchant Rewards */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Spending Categories */}
                <div className="bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-4 h-80">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Spending Categories</h3>
                  {cardData.spending_categories && cardData.spending_categories.length > 0 ? (
                    <div className="space-y-3">
                      <div className={`space-y-3 ${showAllCategories ? 'h-64 overflow-y-auto' : 'h-48 overflow-hidden'}`}>
                        {cardData.spending_categories.slice(0, showAllCategories ? undefined : 4).map((category) => (
                          <div key={category.id} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-600 rounded-lg">
                            <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                              {category.category_display_name.replace(/_/g, ' ')}
                            </span>
                            <span className="text-sm text-green-600 dark:text-green-400 font-semibold">
                              {category.reward_display}
                            </span>
                          </div>
                        ))}
                      </div>
                      
                      {cardData.spending_categories.length > 4 && (
                        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                          <button
                            onClick={() => setShowAllCategories(!showAllCategories)}
                            className="w-full flex items-center justify-center space-x-2 text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors"
                          >
                            <span>{showAllCategories ? 'See Less' : `See More (${cardData.spending_categories.length - 4} more)`}</span>
                            {showAllCategories ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                          </button>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400 text-sm">No spending categories available</p>
                  )}
                </div>

                {/* Merchant Rewards */}
                <div className="bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-4 h-80">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Merchant Rewards</h3>
                  {cardData.merchant_rewards && cardData.merchant_rewards.length > 0 ? (
                    <div className="space-y-3">
                      <div className={`space-y-3 ${showAllMerchants ? 'h-64 overflow-y-auto' : 'h-48 overflow-hidden'}`}>
                        {cardData.merchant_rewards.slice(0, showAllMerchants ? undefined : 4).map((merchant) => (
                          <div key={merchant.id} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-600 rounded-lg">
                            <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                              {merchant.merchant_display_name.replace(/_/g, ' ')}
                            </span>
                            <span className="text-sm text-blue-600 dark:text-blue-400 font-semibold">
                              {merchant.reward_display}
                            </span>
                          </div>
                        ))}
                      </div>
                      
                      {cardData.merchant_rewards.length > 4 && (
                        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                          <button
                            onClick={() => setShowAllMerchants(!showAllMerchants)}
                            className="w-full flex items-center justify-center space-x-2 text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium transition-colors"
                          >
                            <span>{showAllMerchants ? 'See Less' : `See More (${cardData.merchant_rewards.length - 4} more)`}</span>
                            {showAllMerchants ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                          </button>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-gray-500 dark:text-gray-400 text-sm">No merchant rewards available</p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Review Section */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
                <Star className="w-5 h-5 mr-2" />
                Review Section
              </h2>
            </div>
            
            <div className="p-6">
              {user && !userReview && (
                <div className="mb-6">
                  <button
                    onClick={() => setShowReviewForm(true)}
                    className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
                  >
                    Write a Review
                  </button>
                </div>
              )}

              {showReviewForm && (
                <div className="mb-6">
                  <ReviewForm
                    onSubmit={handleReviewSubmit}
                    onCancel={() => setShowReviewForm(false)}
                    initialData={userReview}
                  />
                </div>
              )}

                             {/* Simple Reviews Display */}
               <div className="space-y-4">
                 {reviews?.reviews && reviews.reviews.length > 0 ? (
                   reviews.reviews.map((review) => (
                     <div key={review.id} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                       <div className="flex justify-between items-start mb-3">
                         <div className="flex items-center space-x-2">
                           <User className="w-4 h-4 text-gray-400" />
                           <span className="font-medium text-gray-900 dark:text-white">{review.user_name}</span>
                           {review.is_verified_cardholder && (
                             <CheckCircle className="w-4 h-4 text-green-500" />
                           )}
                         </div>
                         <div className="flex items-center space-x-1">
                           {[1, 2, 3, 4, 5].map((star) => (
                             <Star
                               key={star}
                               className={`w-4 h-4 ${
                                 star <= review.overall_rating
                                   ? 'text-yellow-400 fill-current'
                                   : 'text-gray-300'
                               }`}
                             />
                           ))}
                         </div>
                       </div>
                       
                       {review.review_title && (
                         <h4 className="font-semibold text-gray-900 dark:text-white mb-2">{review.review_title}</h4>
                       )}
                       
                       {review.review_content && (
                         <p className="text-gray-700 dark:text-gray-300 mb-3">{review.review_content}</p>
                       )}
                       
                       <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                         {review.pros && (
                           <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
                             <h5 className="font-medium text-green-800 dark:text-green-200 mb-1">Pros</h5>
                             <p className="text-green-700 dark:text-green-300 text-sm">{review.pros}</p>
                           </div>
                         )}
                         
                         {review.cons && (
                           <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
                             <h5 className="font-medium text-red-800 dark:text-red-200 mb-1">Cons</h5>
                             <p className="text-red-700 dark:text-red-300 text-sm">{review.cons}</p>
                           </div>
                         )}
                       </div>
                       
                       {review.experience && (
                         <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                           <h5 className="font-medium text-blue-800 dark:text-blue-200 mb-1">Experience</h5>
                           <p className="text-blue-700 dark:text-blue-300 text-sm">{review.experience}</p>
                         </div>
                       )}
                       
                       <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                         <span className="text-xs text-gray-500 dark:text-gray-400">
                           {new Date(review.created_at).toLocaleDateString()}
                         </span>
                         <div className="flex items-center space-x-2">
                           <button
                             onClick={() => handleVote(review.id.toString(), 'helpful')}
                             className="flex items-center space-x-1 text-xs text-gray-500 hover:text-green-600 dark:hover:text-green-400"
                           >
                             <ThumbsUp className="w-3 h-3" />
                             <span>Helpful ({review.helpful_votes})</span>
                           </button>
                         </div>
                       </div>
                     </div>
                   ))
                 ) : (
                   <div className="text-center py-8">
                     <div className="text-gray-500 dark:text-gray-400 text-lg mb-2">No reviews yet</div>
                     <div className="text-gray-400 dark:text-gray-500 text-sm">
                       Be the first to share your experience with this card!
                     </div>
                   </div>
                 )}
               </div>
            </div>
          </div>

          {/* Section 3: Community Discussion */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="p-6 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center">
                  <MessageSquare className="w-5 h-5 mr-2" />
                  Community Discussion
                </h2>
                <button
                  onClick={() => navigate(`/community/${cardId}`)}
                  className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors text-sm"
                >
                  Join Discussion
                </button>
              </div>
            </div>
            
            <div className="p-6">
              <div className="text-center py-8">
                <MessageSquare className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  Join the community discussion! Share your experiences, ask questions, and connect with other card users.
                </p>
                <div className="flex items-center justify-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center">
                    <ThumbsUp className="w-4 h-4 mr-1" />
                    <span>Upvote</span>
                  </div>
                  <div className="flex items-center">
                    <ThumbsDown className="w-4 h-4 mr-1" />
                    <span>Downvote</span>
                  </div>
                  <div className="flex items-center">
                    <MessageSquare className="w-4 h-4 mr-1" />
                    <span>Reply</span>
                  </div>
                </div>
                <div className="mt-6">
                  <button
                    onClick={() => navigate(`/community/${cardId}`)}
                    className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
                  >
                    Start Discussion
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardDetailPage; 