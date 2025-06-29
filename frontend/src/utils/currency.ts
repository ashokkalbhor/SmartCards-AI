/**
 * Currency formatting utilities for Indian Rupees
 */

/**
 * Format amount in Indian Rupees with proper comma separation
 * @param amount - The amount to format
 * @param showDecimals - Whether to show decimal places
 * @returns Formatted currency string
 */
export const formatCurrency = (amount: number, showDecimals: boolean = true): string => {
  const options: Intl.NumberFormatOptions = {
    style: 'currency',
    currency: 'INR',
    currencyDisplay: 'symbol',
    minimumFractionDigits: showDecimals ? 2 : 0,
    maximumFractionDigits: showDecimals ? 2 : 0,
  };

  // Use Indian number format
  return new Intl.NumberFormat('en-IN', options).format(amount);
};

/**
 * Format amount with rupee symbol only (no currency formatting)
 * @param amount - The amount to format
 * @param showDecimals - Whether to show decimal places
 * @returns Formatted string with rupee symbol
 */
export const formatRupees = (amount: number, showDecimals: boolean = true): string => {
  const formatted = showDecimals 
    ? amount.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : amount.toLocaleString('en-IN');
  
  return `₹${formatted}`;
};

/**
 * Format amount for display with Indian number system
 * @param amount - The amount to format
 * @returns Formatted number string
 */
export const formatIndianNumber = (amount: number): string => {
  return amount.toLocaleString('en-IN');
}; 