import React, { useState, useRef, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Send, Bot, User, Zap, Database, Clock, TrendingUp, History, MessageSquare, AlertCircle } from 'lucide-react';
import { sqlAgentServiceAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';

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


interface Conversation {
  id: number;
  user_id: number;
  title: string;
  conversation_type: string;
  status: string;
  message_count: number;
  created_at: string;
  updated_at: string;
  last_message_at: string;
}

const EnhancedChatBot: React.FC = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<EnhancedMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [stats, setStats] = useState({
    totalProcessingTime: 0,
    totalQueries: 0
  });
  const [hasChatAccess, setHasChatAccess] = useState<boolean | null>(null);
  const [isRequestingAccess, setIsRequestingAccess] = useState(false);
  const [accessRequested, setAccessRequested] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Check chat access status
  const checkChatAccess = useCallback(async () => {
    if (!user?.id) return;
    
    try {
      const response = await sqlAgentServiceAPI.getChatAccessStatus();
      setHasChatAccess(response.has_access);
    } catch (error) {
      console.error('Error checking chat access:', error);
      setHasChatAccess(false);
    }
  }, [user?.id]);

  const loadChatHistory = useCallback(async () => {
    if (!user?.id) return;
    
    setIsLoadingHistory(true);
    try {
      // Get user's conversations
      const conversationsResponse = await sqlAgentServiceAPI.getConversations(user.id);
      setConversations(conversationsResponse.conversations || []);
      
      // Load the most recent conversation
      if (conversationsResponse.conversations && conversationsResponse.conversations.length > 0) {
        const latestConversation = conversationsResponse.conversations[0];
        setCurrentConversationId(latestConversation.id);
        
        // Load messages for the latest conversation
        const historyResponse = await sqlAgentServiceAPI.getChatHistory(latestConversation.id);
        if (historyResponse.messages && historyResponse.messages.length > 0) {
          const formattedMessages = historyResponse.messages.map((msg: any) => ({
            id: msg.id,
            text: msg.content,
            isUser: msg.role === 'user',
            timestamp: new Date(msg.created_at),
            source: msg.role === 'user' ? 'user' : 'history',
            confidence: 1.0,
            processingTime: msg.response_time,
            sqlQuery: msg.message_metadata?.sql_query,
            explanation: msg.message_metadata?.explanation
          }));
          
          setMessages(formattedMessages);
        } else {
          // No history, show welcome message
          setMessages([{
            id: 1,
            text: "Hello! I'm your SmartCards AI assistant. I can help you with credit card recommendations, spending analysis, and reward optimization. How can I assist you today?",
            isUser: false,
            timestamp: new Date(),
            source: "welcome",
            confidence: 1.0
          }]);
        }
      } else {
        // No conversations, show welcome message
        setMessages([{
          id: 1,
          text: "Hello! I'm your SmartCards AI assistant. I can help you with credit card recommendations, spending analysis, and reward optimization. How can I assist you today?",
          isUser: false,
          timestamp: new Date(),
          source: "welcome",
          confidence: 1.0
        }]);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
      // Show welcome message on error
      setMessages([{
        id: 1,
        text: "Hello! I'm your SmartCards AI assistant. I can help you with credit card recommendations, spending analysis, and reward optimization. How can I assist you today?",
        isUser: false,
        timestamp: new Date(),
        source: "welcome",
        confidence: 1.0
      }]);
    } finally {
      setIsLoadingHistory(false);
    }
  }, [user?.id]);

  // Request chat access
  const requestChatAccess = async () => {
    if (!user?.id) return;
    
    setIsRequestingAccess(true);
    try {
      await sqlAgentServiceAPI.requestChatAccess();
      setAccessRequested(true);
      // Show success message
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: "Chat access request submitted successfully! You'll be able to use the chat once approved by an admin.",
        isUser: false,
        timestamp: new Date(),
        source: "system"
      }]);
    } catch (error) {
      console.error('Error requesting chat access:', error);
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: "Failed to submit chat access request. Please try again.",
        isUser: false,
        timestamp: new Date(),
        source: "system"
      }]);
    } finally {
      setIsRequestingAccess(false);
    }
  };

  // Load chat history when component mounts or user changes
  useEffect(() => {
    if (user?.id) {
      loadChatHistory();
      checkChatAccess();
    } else {
      // Show welcome message for non-authenticated users
      setMessages([{
        id: 1,
        text: "Hello! I'm your SmartCards AI assistant. I can help you with credit card recommendations, spending analysis, and reward optimization. Please log in to access your personalized chat history and portfolio information.",
        isUser: false,
        timestamp: new Date(),
        source: "welcome",
        confidence: 1.0
      }]);
    }
  }, [user?.id, loadChatHistory, checkChatAccess]);

  const createNewConversation = async () => {
    if (!user?.id) return null;
    
    try {
      const response = await sqlAgentServiceAPI.createConversation({
        title: `Chat ${new Date().toLocaleDateString()}`,
        conversation_type: "card_recommendation"
      });
      setCurrentConversationId(response.id);
      return response.id;
    } catch (error) {
      console.error('Error creating conversation:', error);
      return null;
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    // Check if user has chat access
    if (hasChatAccess === false) {
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: "You don't have chat access yet. Please request access to use the chat feature.",
        isUser: false,
        timestamp: new Date(),
        source: "system"
      }]);
      return;
    }

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
      // Use actual user ID instead of hardcoded value
      const userId = user?.id || 1; // Fallback for non-authenticated users
      
      // Create conversation if none exists
      let conversationId = currentConversationId;
      if (!conversationId && user?.id) {
        conversationId = await createNewConversation();
      }

      const response = await sqlAgentServiceAPI.processQuery({
        query: inputMessage,
        user_id: userId,
        context: {
          user_cards: [], // Will be populated by SQL agent from database
          conversation_id: conversationId
        },
        include_sql: true,
        include_explanation: true,
        max_results: 10
      });

      // Clean and format the response
      const cleanedResponse = cleanResponseText(response.response);

      const botResponse: EnhancedMessage = {
        id: Date.now() + 1,
        text: cleanedResponse,
        isUser: false,
        timestamp: new Date(),
        source: response.source,
        confidence: response.confidence,
        processingTime: response.processing_time,
        sqlQuery: response.sql_query,
        explanation: response.explanation
      };

      setMessages(prev => [...prev, botResponse]);

      // Save messages to database if user is authenticated
      if (user?.id && conversationId) {
        try {
          // Save user message
          await sqlAgentServiceAPI.saveMessage(conversationId, {
            role: 'user',
            content: inputMessage,
            message_type: 'text'
          });

          // Save bot response
          await sqlAgentServiceAPI.saveMessage(conversationId, {
            role: 'assistant',
            content: response.response,
            message_type: 'text',
            response_time: response.processing_time,
            message_metadata: {
              sql_query: response.sql_query,
              explanation: response.explanation,
              confidence: response.confidence
            }
          });
        } catch (saveError) {
          console.error('Error saving messages:', saveError);
          // Don't fail the entire operation if saving fails
        }
      }

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

  // Clean response text to remove raw JSON and improve formatting
  const cleanResponseText = (text: string): string => {
    if (!text) return '';
    
    // Remove raw JSON-like strings that appear in responses
    let cleaned = text.replace(/I found \d+ results:.*?\{.*?\}/gs, '');
    
    // Remove any remaining raw JSON patterns
    cleaned = cleaned.replace(/\{.*?"result".*?\}/gs, '');
    
    // Clean up multiple newlines
    cleaned = cleaned.replace(/\n{3,}/g, '\n\n');
    
    // Remove trailing whitespace
    cleaned = cleaned.trim();
    
    return cleaned;
  };

  const getSourceIcon = (source: string) => {
    switch (source) {
      case 'cache':
        return <Database className="h-3 w-3" />;
      case 'sql_agent':
        return <Bot className="h-3 w-3" />;
      case 'welcome':
        return <Bot className="h-3 w-3" />;
      case 'history':
        return <History className="h-3 w-3" />;
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
      case 'history':
        return 'text-blue-600';
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
      case 'history':
        return 'History';
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

  // Render chat access request UI
  const renderChatAccessRequest = () => (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-full min-h-[600px] flex items-center justify-center">
      <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-8 max-w-md text-center">
        <AlertCircle className="h-16 w-16 text-yellow-600 dark:text-yellow-400 mx-auto mb-4" />
        <h3 className="text-xl font-semibold text-yellow-800 dark:text-yellow-200 mb-3">
          Chat Access Required
        </h3>
        <p className="text-yellow-700 dark:text-yellow-300 mb-6">
          You need admin approval to use the chat feature. Click below to request access.
        </p>
        <button
          onClick={requestChatAccess}
          disabled={isRequestingAccess || accessRequested}
          className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-yellow-400 text-white px-8 py-3 rounded-lg font-medium transition-colors"
        >
          {isRequestingAccess ? 'Requesting...' : accessRequested ? 'Request Submitted' : 'Request Chat Access'}
        </button>
        {accessRequested && (
          <p className="text-sm text-yellow-600 dark:text-yellow-400 mt-4">
            Your request has been submitted. You'll be notified once approved.
          </p>
        )}
      </div>
    </div>
  );

  if (isLoadingHistory) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 h-full min-h-[600px] flex items-center justify-center">
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-600"></div>
          <span className="text-gray-600 dark:text-gray-400">Loading chat history...</span>
        </div>
      </div>
    );
  }

  // Show chat access request if user doesn't have access
  if (hasChatAccess === false) {
    return renderChatAccessRequest();
  }

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
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {user ? `Welcome back, ${user.first_name || user.email}!` : 'Ask me about your cards and spending'}
            </p>
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
          {conversations.length > 0 && (
            <div className="flex items-center space-x-1">
              <MessageSquare className="h-3 w-3" />
              <span>{conversations.length} chats</span>
            </div>
          )}
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
            placeholder={user ? "Ask me about your cards, spending, or rewards..." : "Please log in to access personalized features..."}
            disabled={!user}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white disabled:bg-gray-100 dark:disabled:bg-gray-800 disabled:cursor-not-allowed"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isTyping || !user}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white rounded-lg transition-colors flex items-center space-x-2"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
          {user ? 'Try: "Which card is best for Amazon?" or "Show my credit cards"' : 'Log in to access your personalized chat history and portfolio'}
        </p>
      </div>
    </div>
  );
};

export default EnhancedChatBot; 