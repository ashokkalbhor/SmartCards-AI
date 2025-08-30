import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, User, Zap, Database, Clock, TrendingUp } from 'lucide-react';
import { sqlAgentServiceAPI } from '../../services/api';

interface EnhancedMessage {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
  source?: string;
  confidence?: number;
  processingTime?: number;
  sqlQuery?: string;
  explanation?: string;
}

interface ChatResponse {
  response: string;
  sql_query?: string;
  results?: any;
  explanation?: string;
  confidence: number;
  processing_time: number;
  source: string;
  metadata?: any;
}

const EnhancedChatBot: React.FC = () => {
  const [messages, setMessages] = useState<EnhancedMessage[]>([
    {
      id: 1,
      text: "Hello! I'm your SmartCards AI assistant. I can help you with credit card recommendations, spending analysis, and reward optimization. How can I assist you today?",
      isUser: false,
      timestamp: new Date(),
      source: "welcome",
      confidence: 1.0
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [stats, setStats] = useState({
    totalProcessingTime: 0,
    totalQueries: 0
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: EnhancedMessage = {
      id: Date.now(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      // Get basic user data from localStorage or use defaults
      const userData = {
        user_id: 1, // Default user ID
        context: {
          user_cards: [] // Will be populated by SQL agent from database
        }
      };

      const response = await sqlAgentServiceAPI.processQuery({
        query: inputMessage,
        user_id: userData.user_id,
        include_sql: true,
        include_explanation: true,
        max_results: 10
      });

      const botResponse: EnhancedMessage = {
        id: Date.now() + 1,
        text: response.response,
        isUser: false,
        timestamp: new Date(),
        source: response.source,
        confidence: response.confidence,
        processingTime: response.processing_time,
        sqlQuery: response.sql_query,
        explanation: response.explanation
      };

      setMessages(prev => [...prev, botResponse]);

      // Update stats
      setStats(prev => ({
        totalProcessingTime: prev.totalProcessingTime + response.processing_time,
        totalQueries: prev.totalQueries + 1
      }));

    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage: EnhancedMessage = {
        id: Date.now() + 1,
        text: "I'm sorry, I'm having trouble processing your request right now. Please try again.",
        isUser: false,
        timestamp: new Date(),
        source: "error",
        confidence: 0.0
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'cache':
        return <Database className="h-3 w-3" />;
      case 'sql_agent':
        return <Bot className="h-3 w-3" />;
      case 'welcome':
        return <Bot className="h-3 w-3" />;
      case 'error':
        return <Zap className="h-3 w-3" />;
      default:
        return <Bot className="h-3 w-3" />;
    }
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'cache':
        return 'text-green-600';
      case 'sql_agent':
        return 'text-purple-600';
      case 'welcome':
        return 'text-gray-600';
      case 'error':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getSourceLabel = (source: string) => {
    switch (source) {
      case 'cache':
        return 'Cached';
      case 'sql_agent':
        return 'AI';
      case 'welcome':
        return 'Welcome';
      case 'error':
        return 'Error';
      default:
        return 'AI';
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Helper function to format text for better readability
  const formatMessageText = (text: string) => {
    if (!text) return '';
    
    // Split by double newlines to separate paragraphs
    const paragraphs = text.split('\n\n');
    
    return paragraphs.map((paragraph, index) => {
      // Handle numbered lists (1. 2. 3. etc.)
      if (/^\d+\./.test(paragraph.trim())) {
        const lines = paragraph.split('\n');
        return (
          <div key={index} className="mb-3">
            {lines.map((line, lineIndex) => {
              const trimmedLine = line.trim();
              if (/^\d+\./.test(trimmedLine)) {
                return (
                  <div key={lineIndex} className="flex items-start mb-2">
                    <span className="font-semibold text-primary-600 dark:text-primary-400 mr-2 min-w-[20px]">
                      {trimmedLine.match(/^\d+/)?.[0]}.
                    </span>
                    <span className="flex-1">{trimmedLine.replace(/^\d+\.\s*/, '')}</span>
                  </div>
                );
              } else if (trimmedLine.startsWith('•') || trimmedLine.startsWith('-')) {
                return (
                  <div key={lineIndex} className="flex items-start mb-1 ml-4">
                    <span className="text-primary-600 dark:text-primary-400 mr-2">•</span>
                    <span className="flex-1">{trimmedLine.replace(/^[•-]\s*/, '')}</span>
                  </div>
                );
              } else if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
                return (
                  <div key={lineIndex} className="font-semibold text-primary-600 dark:text-primary-400 mb-2">
                    {trimmedLine.replace(/\*\*/g, '')}
                  </div>
                );
              } else if (trimmedLine) {
                return <div key={lineIndex} className="mb-2">{trimmedLine}</div>;
              }
              return null;
            })}
          </div>
        );
      }
      
      // Handle bullet points
      if (paragraph.includes('•') || paragraph.includes('-')) {
        const lines = paragraph.split('\n');
        return (
          <div key={index} className="mb-3">
            {lines.map((line, lineIndex) => {
              const trimmedLine = line.trim();
              if (trimmedLine.startsWith('•') || trimmedLine.startsWith('-')) {
                return (
                  <div key={lineIndex} className="flex items-start mb-1">
                    <span className="text-primary-600 dark:text-primary-400 mr-2">•</span>
                    <span className="flex-1">{trimmedLine.replace(/^[•-]\s*/, '')}</span>
                  </div>
                );
              } else if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
                return (
                  <div key={lineIndex} className="font-semibold text-primary-600 dark:text-primary-400 mb-2">
                    {trimmedLine.replace(/\*\*/g, '')}
                  </div>
                );
              } else if (trimmedLine) {
                return <div key={lineIndex} className="mb-2">{trimmedLine}</div>;
              }
              return null;
            })}
          </div>
        );
      }
      
      // Handle bold text
      if (paragraph.includes('**')) {
        const parts = paragraph.split(/(\*\*.*?\*\*)/g);
        return (
          <div key={index} className="mb-3">
            {parts.map((part, partIndex) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return (
                  <span key={partIndex} className="font-semibold text-primary-600 dark:text-primary-400">
                    {part.replace(/\*\*/g, '')}
                  </span>
                );
              }
              return <span key={partIndex}>{part}</span>;
            })}
          </div>
        );
      }
      
      // Regular paragraph
      return <div key={index} className="mb-3">{paragraph}</div>;
    });
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-full min-h-[600px] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-primary-600 rounded-full flex items-center justify-center">
            <Bot className="h-6 w-6 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">SmartCards AI Assistant</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">Ask me about your cards and spending</p>
          </div>
        </div>
        
        {/* Stats */}
        <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
          <div className="flex items-center space-x-1">
            <TrendingUp className="h-3 w-3" />
            <span>{stats.totalQueries} queries</span>
          </div>
          <div className="flex items-center space-x-1">
            <Clock className="h-3 w-3" />
            <span>{(stats.totalProcessingTime / 1000).toFixed(1)}s</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
            {...({} as any)}
          >
            <div className={`flex items-end space-x-2 max-w-[80%] ${message.isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${message.isUser ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-600'}`}>
                {message.isUser ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  getSourceIcon(message.source || 'bot')
                )}
              </div>
              <div className={`rounded-lg px-4 py-2 ${message.isUser 
                ? 'bg-primary-600 text-white' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
              }`}>
                <div className="text-sm">
                  {message.isUser ? message.text : formatMessageText(message.text)}
                </div>
                <div className="flex items-center justify-between mt-2">
                  <p className={`text-xs ${message.isUser 
                    ? 'text-primary-100' 
                    : 'text-gray-500 dark:text-gray-400'
                  }`}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                  {!message.isUser && message.source && (
                    <div className={`flex items-center space-x-1 text-xs ${getSourceColor(message.source)}`}>
                      {getSourceIcon(message.source)}
                      <span>{getSourceLabel(message.source)}</span>
                    </div>
                  )}
                </div>
                {!message.isUser && message.processingTime && (
                  <p className="text-xs text-gray-400 mt-1">
                    {(message.processingTime * 1000).toFixed(0)}ms
                  </p>
                )}
              </div>
            </div>
          </motion.div>
        ))}
        
        {isTyping && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
            {...({} as any)}
          >
            <div className="flex items-end space-x-2">
              <div className="w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded-full flex items-center justify-center">
                <Bot className="h-4 w-4 text-gray-600 dark:text-gray-300" />
              </div>
              <div className="bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about your cards, spending, or rewards..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isTyping}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
          Try: "Which card is best for Amazon?" or "Show my credit cards"
        </p>
      </div>
    </div>
  );
};

export default EnhancedChatBot; 