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
}

const EditableRewardsSection: React.FC<EditableRewardsSectionProps> = ({
  title,
  items,
  type,
  onEdit,
  isEditable = true
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedItems, setEditedItems] = useState<RewardItem[]>(items);

  const handleEdit = () => {
    setIsEditing(true);
    setEditedItems([...items]);
  };

  const handleSave = () => {
    setIsEditing(false);
    onEdit?.(editedItems);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedItems(items);
  };

  const handleItemChange = (index: number, field: keyof RewardItem, value: any) => {
    const updatedItems = [...editedItems];
    updatedItems[index] = { ...updatedItems[index], [field]: value };
    setEditedItems(updatedItems);
  };

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
          {isEditable && !isEditing && (
            <button
              onClick={handleEdit}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors text-sm flex items-center"
            >
              <Edit3 className="w-4 h-4 mr-1" />
              Edit
            </button>
          )}
          {isEditing && (
            <div className="flex space-x-2">
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors text-sm flex items-center"
              >
                <Check className="w-4 h-4 mr-1" />
                Save
              </button>
              <button
                onClick={handleCancel}
                className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors text-sm flex items-center"
              >
                <X className="w-4 h-4 mr-1" />
                Cancel
              </button>
            </div>
          )}
        </div>
      </div>
      
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg border ${getItemBackground(item)} transition-colors`}
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
                  {getRewardDisplay(item)}
                </div>
                
                {!isNotAvailable(item) && item.reward_cap && (
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Cap:</span>
                    <span className="text-sm text-gray-900 dark:text-white">
                      ₹{item.reward_cap.toLocaleString()}/{item.reward_cap_period}
                    </span>
                  </div>
                )}
                
                {isEditing && !isNotAvailable(item) && (
                  <div className="space-y-2 pt-2 border-t border-gray-200 dark:border-gray-600">
                    <div>
                      <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Reward Rate (%)
                      </label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        max="100"
                        value={item.reward_rate}
                        onChange={(e) => handleItemChange(index, 'reward_rate', parseFloat(e.target.value) || 0)}
                        className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                        Reward Type
                      </label>
                      <select
                        value={item.reward_type}
                        onChange={(e) => handleItemChange(index, 'reward_type', e.target.value)}
                        className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                      >
                        <option value="points">Points</option>
                        <option value="cashback">Cashback</option>
                        <option value="rewards">Rewards</option>
                      </select>
                    </div>
                    
                    {item.reward_cap !== undefined && (
                      <div>
                        <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                          Reward Cap (₹)
                        </label>
                        <input
                          type="number"
                          min="0"
                          value={item.reward_cap || ''}
                          onChange={(e) => handleItemChange(index, 'reward_cap', parseFloat(e.target.value) || null)}
                          className="w-full px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                        />
                      </div>
                    )}
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