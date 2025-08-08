import React, { useState } from 'react';
import { Edit3, Check, X, Plus } from 'lucide-react';

interface RewardItem {
  id?: number;
  category_name?: string;
  category_display_name?: string;
  merchant_name?: string;
  merchant_display_name?: string;
  merchant_category?: string;
  reward_rate: number;
  reward_type: string;
  reward_cap?: number | null;
  reward_cap_period?: string | null;
  is_active: boolean;
  is_editable?: boolean;
  reward_display: string;
  additional_conditions?: string;
}

interface EditableRewardsSectionProps {
  title: string;
  items: RewardItem[];
  type: 'spending' | 'merchant';
  onEdit?: (items: RewardItem[]) => void;
  isEditable?: boolean;
  onEditSuggestion?: (fieldType: 'spending_category' | 'merchant_reward', fieldName: string, currentValue: string) => void;
}

const EditableRewardsSection: React.FC<EditableRewardsSectionProps> = ({
  title,
  items,
  type,
  onEdit,
  isEditable = true,
  onEditSuggestion
}) => {


  const isNotAvailable = (item: RewardItem) => {
    return item.reward_display === "Not Available" || !item.is_active;
  };

  const getRewardDisplay = (item: RewardItem) => {
    if (isNotAvailable(item)) {
      return (
        <span className="text-gray-500 dark:text-gray-400 italic">
          Not Available
        </span>
      );
    }
    return (
      <span className="font-medium text-green-600 dark:text-green-400">
        {item.reward_display}
      </span>
    );
  };

  const getItemBackground = (item: RewardItem) => {
    if (isNotAvailable(item)) {
      return "bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700";
    }
    return "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-700";
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              {title}
            </h2>
          </div>
        </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item, index) => (
                            <div
                  key={index}
                  className={`p-4 rounded-lg border ${getItemBackground(item)} transition-colors group`}
                >
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {type === 'spending' ? item.category_display_name : item.merchant_display_name}
                  </h3>
                  {type === 'merchant' && item.merchant_category && (
                    <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                      {item.merchant_category.replace('_', ' ')}
                    </p>
                  )}
                </div>
                {isNotAvailable(item) && (
                  <span className="text-xs bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 px-2 py-1 rounded">
                    Not Available
                  </span>
                )}
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">Reward:</span>
                  <div className="flex items-center space-x-2">
                    {getRewardDisplay(item)}
                    {isEditable && onEditSuggestion && (
                      <button
                        onClick={() => onEditSuggestion(
                          type === 'spending' ? 'spending_category' : 'merchant_reward',
                          type === 'spending' ? item.category_name! : item.merchant_name!,
                          isNotAvailable(item) ? '0' : item.reward_rate.toString()
                        )}
                        className="opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-primary-600 dark:hover:text-primary-400"
                        title="Suggest edit"
                      >
                        <Edit3 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
                
                {!isNotAvailable(item) && item.reward_cap && (
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Cap:</span>
                    <span className="text-sm text-gray-900 dark:text-white">
                      ₹{item.reward_cap.toLocaleString()}/{item.reward_cap_period}
                    </span>
                  </div>
                )}
                

              </div>
            </div>
          ))}
        </div>
        
        {items.length === 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500 dark:text-gray-400">
              No {type === 'spending' ? 'spending categories' : 'merchant rewards'} available.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default EditableRewardsSection; 