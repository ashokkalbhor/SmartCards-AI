import React, { useState } from 'react';

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
  };

  const handleSave = () => {
    if (onEdit) {
      onEdit(editedItems);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedItems(items);
    setIsEditing(false);
  };

  const updateItem = (index: number, field: keyof RewardItem, value: any) => {
    const newItems = [...editedItems];
    newItems[index] = { ...newItems[index], [field]: value };
    setEditedItems(newItems);
  };

  const addItem = () => {
    const newItem: RewardItem = {
      reward_rate: 1.0,
      reward_type: 'points',
      is_active: true,
      is_editable: true
    };
    setEditedItems([...editedItems, newItem]);
  };

  const removeItem = (index: number) => {
    const newItems = editedItems.filter((_, i) => i !== index);
    setEditedItems(newItems);
  };

  if (items.length === 0 && !isEditing) {
    return (
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          {isEditable && (
            <button
              onClick={handleEdit}
              className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              Add {type === 'spending' ? 'Categories' : 'Merchants'}
            </button>
          )}
        </div>
        <div className="text-gray-500 text-center py-4">
          No {type === 'spending' ? 'spending categories' : 'merchant rewards'} available yet.
          {isEditable && (
            <span className="block mt-2 text-sm">
              Click "Add {type === 'spending' ? 'Categories' : 'Merchants'}" to get started.
            </span>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        {isEditable && (
          <div className="flex space-x-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSave}
                  className="text-green-600 hover:text-green-800 text-sm font-medium"
                >
                  Save
                </button>
                <button
                  onClick={handleCancel}
                  className="text-gray-600 hover:text-gray-800 text-sm font-medium"
                >
                  Cancel
                </button>
              </>
            ) : (
              <button
                onClick={handleEdit}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                Edit
              </button>
            )}
          </div>
        )}
      </div>

      <div className="space-y-4">
        {(isEditing ? editedItems : items).map((item, index) => (
          <div key={index} className="border rounded-lg p-4 bg-gray-50">
            {isEditing ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {type === 'spending' ? 'Category' : 'Merchant'}
                  </label>
                  <input
                    type="text"
                    value={type === 'spending' ? item.category_display_name || '' : item.merchant_display_name || ''}
                    onChange={(e) => updateItem(index, type === 'spending' ? 'category_display_name' : 'merchant_display_name', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={type === 'spending' ? 'e.g., Dining' : 'e.g., Amazon'}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Reward Rate
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={item.reward_rate}
                    onChange={(e) => updateItem(index, 'reward_rate', parseFloat(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Reward Type
                  </label>
                  <select
                    value={item.reward_type}
                    onChange={(e) => updateItem(index, 'reward_type', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="points">Points</option>
                    <option value="cashback">Cashback</option>
                    <option value="miles">Miles</option>
                  </select>
                </div>
                <div className="md:col-span-3 flex justify-between items-center">
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={item.is_active}
                      onChange={(e) => updateItem(index, 'is_active', e.target.checked)}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Active</span>
                  </label>
                  <button
                    onClick={() => removeItem(index)}
                    className="text-red-600 hover:text-red-800 text-sm font-medium"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex justify-between items-center">
                <div>
                  <h4 className="font-medium text-gray-900">
                    {type === 'spending' ? item.category_display_name : item.merchant_display_name}
                  </h4>
                  <p className="text-sm text-gray-600">
                    {item.reward_rate} {item.reward_type} per ₹100
                  </p>
                </div>
                <div className="text-right">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    item.is_active 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {item.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </div>
            )}
          </div>
        ))}
        
        {isEditing && (
          <button
            onClick={addItem}
            className="w-full py-2 px-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-gray-400 hover:text-gray-700 transition-colors"
          >
            + Add {type === 'spending' ? 'Category' : 'Merchant'}
          </button>
        )}
      </div>
    </div>
  );
};

export default EditableRewardsSection; 