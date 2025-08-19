# 100 Gen AI Interview Questions for Senior Architect Role
## Based on SmartCards AI Project Implementation

### Part 4: Frontend Integration & Advanced Topics (Questions 43-60)

---

## 43. **How would you integrate Gen AI into a React frontend for real-time chat?**

**Answer:** Use WebSocket connections, streaming responses, and state management.

**Example from SmartCards AI:**
```typescript
// frontend/src/hooks/useAIChat.ts
import { useState, useCallback, useRef } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: any;
}

export const useAIChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useMutation({
    mutationFn: async (message: string) => {
      const controller = new AbortController();
      abortControllerRef.current = controller;

      const response = await fetch('/api/v1/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ message }),
        signal: controller.signal
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      let assistantMessage = '';
      setIsStreaming(true);

      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              assistantMessage += data.content;
              
              // Update the last message in real-time
              setMessages(prev => 
                prev.map(msg => 
                  msg.id === 'current' 
                    ? { ...msg, content: assistantMessage }
                    : msg
                )
              );
            } catch (e) {
              console.error('Error parsing stream data:', e);
            }
          }
        }
      }

      setIsStreaming(false);
      return assistantMessage;
    },
    onSuccess: (response) => {
      // Replace the streaming message with the final one
      setMessages(prev => 
        prev.map(msg => 
          msg.id === 'current' 
            ? { ...msg, id: Date.now().toString(), content: response }
            : msg
        )
      );
    },
    onError: (error) => {
      setIsStreaming(false);
      console.error('Chat error:', error);
    }
  });

  const addMessage = useCallback((content: string, role: 'user' | 'assistant') => {
    const newMessage: ChatMessage = {
      id: role === 'assistant' ? 'current' : Date.now().toString(),
      role,
      content,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, newMessage]);
  }, []);

  const sendUserMessage = useCallback(async (message: string) => {
    addMessage(message, 'user');
    sendMessage.mutate(message);
  }, [addMessage, sendMessage]);

  const stopStreaming = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsStreaming(false);
    }
  }, []);

  return {
    messages,
    isStreaming,
    sendUserMessage,
    stopStreaming,
    isLoading: sendMessage.isPending
  };
};
```

---

## 44. **How would you implement error handling and fallback strategies in a Gen AI application?**

**Answer:** Use multiple fallback layers, graceful degradation, and user-friendly error messages.

**Example from SmartCards AI:**
```python
# error_handling/fallback_strategy.py
from typing import Dict, Optional, List
import asyncio
from enum import Enum

class FallbackLevel(Enum):
    CACHE = "cache"
    PATTERN_MATCHING = "pattern_matching"
    SIMPLE_RESPONSE = "simple_response"
    HUMAN_SUPPORT = "human_support"

class FallbackStrategy:
    def __init__(self):
        self.fallback_responses = {
            "openai_error": "I'm having trouble connecting to my knowledge base. Let me try a different approach.",
            "rate_limit": "I'm receiving too many requests right now. Please try again in a moment.",
            "invalid_input": "I didn't understand that. Could you rephrase your question?",
            "general_error": "Something went wrong. I'm here to help with credit card recommendations."
        }
    
    async def process_with_fallbacks(self, user_query: str, user_id: int) -> Dict:
        """Process query with multiple fallback strategies"""
        
        # Level 1: Try OpenAI API
        try:
            response = await self._try_openai_api(user_query, user_id)
            return {**response, "fallback_level": None}
        except Exception as e:
            logger.warning(f"OpenAI API failed: {e}")
        
        # Level 2: Try cache
        try:
            cached_response = await self._try_cache(user_query, user_id)
            if cached_response:
                return {**cached_response, "fallback_level": FallbackLevel.CACHE}
        except Exception as e:
            logger.warning(f"Cache fallback failed: {e}")
        
        # Level 3: Try pattern matching
        try:
            pattern_response = await self._try_pattern_matching(user_query)
            if pattern_response:
                return {**pattern_response, "fallback_level": FallbackLevel.PATTERN_MATCHING}
        except Exception as e:
            logger.warning(f"Pattern matching failed: {e}")
        
        # Level 4: Simple response
        try:
            simple_response = await self._generate_simple_response(user_query)
            return {**simple_response, "fallback_level": FallbackLevel.SIMPLE_RESPONSE}
        except Exception as e:
            logger.error(f"All fallbacks failed: {e}")
        
        # Level 5: Human support
        return {
            "response": "I'm experiencing technical difficulties. Please contact our support team for immediate assistance.",
            "fallback_level": FallbackLevel.HUMAN_SUPPORT,
            "escalate_to_human": True
        }
    
    async def _try_openai_api(self, query: str, user_id: int) -> Dict:
        """Try OpenAI API with timeout and retries"""
        for attempt in range(3):
            try:
                response = await asyncio.wait_for(
                    self.openai_client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": query}],
                        temperature=0.3
                    ),
                    timeout=10.0
                )
                return {
                    "response": response.choices[0].message.content,
                    "source": "openai",
                    "attempt": attempt + 1
                }
            except asyncio.TimeoutError:
                logger.warning(f"OpenAI timeout on attempt {attempt + 1}")
                if attempt == 2:
                    raise
            except Exception as e:
                logger.error(f"OpenAI error on attempt {attempt + 1}: {e}")
                if attempt == 2:
                    raise
                await asyncio.sleep(1)  # Brief delay before retry
    
    async def _try_cache(self, query: str, user_id: int) -> Optional[Dict]:
        """Try to get response from cache"""
        cache_key = self._generate_cache_key(query, user_id)
        cached = await self.cache.get(cache_key)
        
        if cached:
            return {
                "response": cached["response"],
                "source": "cache",
                "cached_at": cached["timestamp"]
            }
        return None
    
    async def _try_pattern_matching(self, query: str) -> Optional[Dict]:
        """Try pattern matching for common queries"""
        patterns = {
            r"best.*card.*for.*amazon": "For Amazon purchases, I recommend using cards with Amazon-specific rewards like the Amazon Pay ICICI Credit Card (5% cashback) or any card with general cashback rewards.",
            r"dining.*card": "For dining, look for cards with dining rewards like HDFC Diners Club (3X rewards) or SBI SimplyCLICK (10X rewards on dining).",
            r"fuel.*card": "For fuel purchases, consider cards like HDFC Bank Regalia (4X rewards on fuel) or ICICI Bank HPCL Coral (4% cashback on fuel)."
        }
        
        for pattern, response in patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                return {
                    "response": response,
                    "source": "pattern_matching",
                    "pattern_matched": pattern
                }
        return None
    
    async def _generate_simple_response(self, query: str) -> Dict:
        """Generate a simple, generic response"""
        if "card" in query.lower() or "credit" in query.lower():
            return {
                "response": "I can help you find the best credit card for your needs. Could you tell me more about your spending habits and preferences?",
                "source": "simple_response"
            }
        else:
            return {
                "response": "I'm here to help with credit card recommendations. What would you like to know?",
                "source": "simple_response"
            }
```

---

## 45. **How would you implement multi-language support in your Gen AI application?**

**Answer:** Use language detection, translation services, and localized prompts.

**Example from SmartCards AI:**
```python
# internationalization/multi_language.py
from typing import Dict, Optional
import langdetect
from googletrans import Translator

class MultiLanguageSupport:
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'bn': 'Bengali',
            'mr': 'Marathi'
        }
        
        # Language-specific prompts
        self.localized_prompts = {
            'en': "You are a credit card expert assistant. Help the user with their query: {query}",
            'hi': "आप एक क्रेडिट कार्ड विशेषज्ञ सहायक हैं। उपयोगकर्ता की मदद करें: {query}",
            'ta': "நீங்கள் ஒரு கிரெடிட் கார்டு நிபுணர் உதவியாளர். பயனருக்கு உதவுங்கள்: {query}",
            'te': "మీరు క్రెడిట్ కార్డ్ నిపుణుడు సహాయకుడు. వినియోగదారుకు సహాయం చేయండి: {query}",
            'bn': "আপনি একজন ক্রেডিট কার্ড বিশেষজ্ঞ সহকারী। ব্যবহারকারীকে সাহায্য করুন: {query}",
            'mr': "तुम्ही क्रेडिट कार्ड तज्ज्ञ सहाय्यक आहात. वापरकर्त्याला मदत करा: {query}"
        }
    
    async def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        try:
            detected = langdetect.detect(text)
            return detected if detected in self.supported_languages else 'en'
        except:
            return 'en'  # Default to English
    
    async def translate_text(self, text: str, target_lang: str, source_lang: str = 'en') -> str:
        """Translate text to target language"""
        if target_lang == source_lang:
            return text
        
        try:
            translation = self.translator.translate(
                text, 
                dest=target_lang, 
                src=source_lang
            )
            return translation.text
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text  # Return original text if translation fails
    
    async def get_localized_prompt(self, query: str, language: str) -> str:
        """Get localized prompt for the AI"""
        if language not in self.localized_prompts:
            language = 'en'  # Fallback to English
        
        return self.localized_prompts[language].format(query=query)
    
    async def process_multilingual_query(self, query: str, user_id: int) -> Dict:
        """Process query in user's preferred language"""
        # Detect language
        detected_lang = await self.detect_language(query)
        
        # Get user's preferred language
        user_pref_lang = await self.get_user_language_preference(user_id)
        target_lang = user_pref_lang or detected_lang
        
        # Translate query to English for processing
        if detected_lang != 'en':
            english_query = await self.translate_text(query, 'en', detected_lang)
        else:
            english_query = query
        
        # Process with AI
        ai_response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": await self.get_localized_prompt(english_query, 'en')
            }],
            temperature=0.3
        )
        
        response_text = ai_response.choices[0].message.content
        
        # Translate response back to user's language
        if target_lang != 'en':
            localized_response = await self.translate_text(response_text, target_lang, 'en')
        else:
            localized_response = response_text
        
        return {
            "response": localized_response,
            "original_language": detected_lang,
            "target_language": target_lang,
            "translated": detected_lang != target_lang,
            "confidence": self._get_translation_confidence(detected_lang, target_lang)
        }
    
    def _get_translation_confidence(self, source_lang: str, target_lang: str) -> float:
        """Get confidence score for translation quality"""
        # Higher confidence for direct language pairs
        confidence_map = {
            ('hi', 'en'): 0.95,  # Hindi to English
            ('ta', 'en'): 0.90,  # Tamil to English
            ('te', 'en'): 0.90,  # Telugu to English
            ('bn', 'en'): 0.85,  # Bengali to English
            ('mr', 'en'): 0.85,  # Marathi to English
        }
        
        return confidence_map.get((source_lang, target_lang), 0.80)
```

---

## 46. **How would you implement real-time collaboration features in your Gen AI application?**

**Answer:** Use WebSocket connections, conflict resolution, and shared state management.

**Example from SmartCards AI:**
```typescript
// frontend/src/hooks/useCollaboration.ts
import { useEffect, useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';

interface CollaborationUser {
  id: string;
  name: string;
  avatar: string;
  cursor: { x: number; y: number } | null;
}

interface SharedDocument {
  id: string;
  content: string;
  version: number;
  lastModified: Date;
  collaborators: CollaborationUser[];
}

export const useCollaboration = (documentId: string) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [collaborators, setCollaborators] = useState<CollaborationUser[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [document, setDocument] = useState<SharedDocument | null>(null);
  const cursorRef = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const newSocket = io(process.env.REACT_APP_WS_URL!, {
      auth: {
        token: localStorage.getItem('token')
      }
    });

    newSocket.on('connect', () => {
      setIsConnected(true);
      newSocket.emit('join-document', { documentId });
    });

    newSocket.on('disconnect', () => {
      setIsConnected(false);
    });

    newSocket.on('user-joined', (user: CollaborationUser) => {
      setCollaborators(prev => [...prev, user]);
    });

    newSocket.on('user-left', (userId: string) => {
      setCollaborators(prev => prev.filter(u => u.id !== userId));
    });

    newSocket.on('cursor-update', ({ userId, cursor }) => {
      setCollaborators(prev => 
        prev.map(u => u.id === userId ? { ...u, cursor } : u)
      );
    });

    newSocket.on('document-update', (updatedDoc: SharedDocument) => {
      setDocument(updatedDoc);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [documentId]);

  const updateCursor = useCallback((x: number, y: number) => {
    cursorRef.current = { x, y };
    socket?.emit('cursor-update', { documentId, cursor: { x, y } });
  }, [socket, documentId]);

  const updateDocument = useCallback((content: string) => {
    socket?.emit('document-update', { 
      documentId, 
      content, 
      version: (document?.version || 0) + 1 
    });
  }, [socket, documentId, document?.version]);

  const sendMessage = useCallback((message: string) => {
    socket?.emit('send-message', { documentId, message });
  }, [socket, documentId]);

  return {
    isConnected,
    collaborators,
    document,
    updateCursor,
    updateDocument,
    sendMessage
  };
};
```

---

## 47. **How would you implement offline support for your Gen AI application?**

**Answer:** Use service workers, local storage, and sync mechanisms.

**Example from SmartCards AI:**
```typescript
// frontend/src/serviceWorker.ts
const CACHE_NAME = 'smartcards-ai-v1';
const OFFLINE_URLS = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/offline.html'
];

self.addEventListener('install', (event: any) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(OFFLINE_URLS))
  );
});

self.addEventListener('fetch', (event: any) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .catch(() => caches.match('/offline.html'))
    );
  } else {
    event.respondWith(
      caches.match(event.request)
        .then(response => response || fetch(event.request))
    );
  }
});

// frontend/src/hooks/useOfflineSupport.ts
import { useState, useEffect } from 'react';

export const useOfflineSupport = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingActions, setPendingActions] = useState<any[]>([]);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  const queueAction = useCallback((action: any) => {
    if (!isOnline) {
      setPendingActions(prev => [...prev, action]);
      localStorage.setItem('pendingActions', JSON.stringify([...pendingActions, action]));
    }
  }, [isOnline, pendingActions]);

  const syncPendingActions = useCallback(async () => {
    if (isOnline && pendingActions.length > 0) {
      for (const action of pendingActions) {
        try {
          await fetch(action.url, action.options);
        } catch (error) {
          console.error('Failed to sync action:', error);
        }
      }
      setPendingActions([]);
      localStorage.removeItem('pendingActions');
    }
  }, [isOnline, pendingActions]);

  useEffect(() => {
    if (isOnline) {
      syncPendingActions();
    }
  }, [isOnline, syncPendingActions]);

  return { isOnline, queueAction, pendingActions };
};
```

---

## 48. **How would you implement performance optimization for your Gen AI application?**

**Answer:** Use caching, lazy loading, and request optimization.

**Example from SmartCards AI:**
```python
# performance/optimizer.py
import asyncio
from functools import lru_cache
from typing import Dict, List
import time

class PerformanceOptimizer:
    def __init__(self):
        self.request_cache = {}
        self.response_cache = {}
        self.batch_queue = []
        self.batch_size = 10
        self.batch_timeout = 0.1  # seconds
    
    @lru_cache(maxsize=1000)
    def get_cached_response(self, query_hash: str) -> Optional[Dict]:
        """Get cached response using LRU cache"""
        return self.response_cache.get(query_hash)
    
    async def batch_process_queries(self, queries: List[str]) -> List[Dict]:
        """Process multiple queries in batch for efficiency"""
        if len(queries) == 1:
            return [await self.process_single_query(queries[0])]
        
        # Group similar queries
        grouped_queries = self._group_similar_queries(queries)
        
        results = []
        for group in grouped_queries:
            # Process similar queries together
            batch_result = await self._process_query_batch(group)
            results.extend(batch_result)
        
        return results
    
    async def _process_query_batch(self, queries: List[str]) -> List[Dict]:
        """Process a batch of similar queries"""
        # Create a single prompt for multiple queries
        combined_prompt = self._create_batch_prompt(queries)
        
        # Make single API call
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": combined_prompt}],
            temperature=0.3
        )
        
        # Parse batch response
        return self._parse_batch_response(response.choices[0].message.content, queries)
    
    def _create_batch_prompt(self, queries: List[str]) -> str:
        """Create a prompt that handles multiple queries"""
        prompt = "Please provide recommendations for the following credit card queries:\n\n"
        for i, query in enumerate(queries, 1):
            prompt += f"{i}. {query}\n"
        prompt += "\nProvide concise, numbered responses for each query."
        return prompt
    
    def _parse_batch_response(self, response: str, queries: List[str]) -> List[Dict]:
        """Parse batch response into individual results"""
        # Simple parsing - split by numbered responses
        lines = response.split('\n')
        results = []
        current_response = ""
        
        for line in lines:
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
                if current_response:
                    results.append({"response": current_response.strip()})
                current_response = line.split('.', 1)[1] if '.' in line else line
            else:
                current_response += " " + line
        
        if current_response:
            results.append({"response": current_response.strip()})
        
        # Ensure we have the right number of results
        while len(results) < len(queries):
            results.append({"response": "Unable to process this query."})
        
        return results[:len(queries)]
    
    async def optimize_prompt(self, query: str) -> str:
        """Optimize prompt for better performance"""
        # Remove unnecessary words
        optimized = re.sub(r'\b(please|kindly|could you|would you)\b', '', query, flags=re.IGNORECASE)
        
        # Add context if missing
        if 'card' not in optimized.lower() and 'credit' not in optimized.lower():
            optimized = f"credit card recommendation: {optimized}"
        
        return optimized.strip()
    
    async def preload_common_responses(self):
        """Preload responses for common queries"""
        common_queries = [
            "best card for Amazon",
            "dining rewards card",
            "fuel credit card",
            "travel credit card",
            "cashback card"
        ]
        
        for query in common_queries:
            response = await self.process_single_query(query)
            query_hash = hashlib.md5(query.encode()).hexdigest()
            self.response_cache[query_hash] = response
```

---

## 49. **How would you implement analytics and user behavior tracking in your Gen AI application?**

**Answer:** Use event tracking, user journey mapping, and performance metrics.

**Example from SmartCards AI:**
```typescript
// frontend/src/analytics/tracker.ts
interface AnalyticsEvent {
  event: string;
  properties: Record<string, any>;
  timestamp: number;
  userId?: string;
  sessionId: string;
}

class AnalyticsTracker {
  private events: AnalyticsEvent[] = [];
  private sessionId: string;
  private userId?: string;

  constructor() {
    this.sessionId = this.generateSessionId();
    this.userId = localStorage.getItem('userId') || undefined;
  }

  track(event: string, properties: Record<string, any> = {}) {
    const analyticsEvent: AnalyticsEvent = {
      event,
      properties,
      timestamp: Date.now(),
      userId: this.userId,
      sessionId: this.sessionId
    };

    this.events.push(analyticsEvent);
    this.sendToAnalytics(analyticsEvent);
  }

  trackChatInteraction(query: string, response: string, processingTime: number) {
    this.track('chat_interaction', {
      query_length: query.length,
      response_length: response.length,
      processing_time: processingTime,
      query_type: this.classifyQuery(query),
      response_quality: this.assessResponseQuality(response)
    });
  }

  trackCardRecommendation(cardName: string, merchant: string, userAction: string) {
    this.track('card_recommendation', {
      card_name: cardName,
      merchant: merchant,
      user_action: userAction,
      recommendation_source: 'ai'
    });
  }

  trackUserJourney(step: string, duration?: number) {
    this.track('user_journey', {
      step,
      duration,
      previous_step: this.getPreviousStep()
    });
  }

  private classifyQuery(query: string): string {
    if (query.toLowerCase().includes('amazon')) return 'merchant_specific';
    if (query.toLowerCase().includes('dining')) return 'category_specific';
    if (query.toLowerCase().includes('best')) return 'recommendation_request';
    return 'general_inquiry';
  }

  private assessResponseQuality(response: string): number {
    // Simple quality assessment
    const hasCardName = /\b[A-Z][a-z]+.*[Cc]ard\b/.test(response);
    const hasPercentage = /\d+%/.test(response);
    const hasActionableInfo = /\b(use|recommend|suggest)\b/i.test(response);
    
    let score = 0;
    if (hasCardName) score += 0.4;
    if (hasPercentage) score += 0.3;
    if (hasActionableInfo) score += 0.3;
    
    return score;
  }

  private async sendToAnalytics(event: AnalyticsEvent) {
    try {
      await fetch('/api/v1/analytics/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event)
      });
    } catch (error) {
      console.error('Analytics tracking failed:', error);
    }
  }
}
```

---

## 50. **How would you implement a recommendation engine that learns from user feedback?**

**Answer:** Use collaborative filtering, content-based filtering, and reinforcement learning.

**Example from SmartCards AI:**
```python
# recommendation/learning_engine.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
import pandas as pd

class RecommendationLearningEngine:
    def __init__(self):
        self.user_preferences = {}
        self.card_features = {}
        self.interaction_matrix = None
        self.feedback_weights = {
            'click': 1.0,
            'like': 2.0,
            'dislike': -1.0,
            'purchase': 5.0,
            'share': 3.0
        }
    
    async def update_user_preferences(self, user_id: int, interaction: Dict):
        """Update user preferences based on interaction"""
        card_id = interaction['card_id']
        action = interaction['action']
        weight = self.feedback_weights.get(action, 0.0)
        
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        if card_id not in self.user_preferences[user_id]:
            self.user_preferences[user_id][card_id] = 0.0
        
        self.user_preferences[user_id][card_id] += weight
        
        # Update interaction matrix
        await self._update_interaction_matrix(user_id, card_id, weight)
    
    async def get_personalized_recommendations(self, user_id: int, context: Dict) -> List[Dict]:
        """Get personalized recommendations using multiple approaches"""
        recommendations = []
        
        # Content-based filtering
        content_based = await self._content_based_filtering(user_id, context)
        recommendations.extend(content_based)
        
        # Collaborative filtering
        collaborative = await self._collaborative_filtering(user_id, context)
        recommendations.extend(collaborative)
        
        # Context-aware filtering
        context_aware = await self._context_aware_filtering(user_id, context)
        recommendations.extend(context_aware)
        
        # Combine and rank recommendations
        ranked_recommendations = await self._rank_recommendations(
            recommendations, user_id, context
        )
        
        return ranked_recommendations[:5]  # Return top 5
    
    async def _content_based_filtering(self, user_id: int, context: Dict) -> List[Dict]:
        """Content-based filtering based on card features"""
        user_profile = await self._build_user_profile(user_id)
        card_scores = {}
        
        for card_id, features in self.card_features.items():
            similarity = cosine_similarity([user_profile], [features])[0][0]
            card_scores[card_id] = similarity
        
        # Sort by similarity score
        sorted_cards = sorted(card_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"card_id": card_id, "score": score, "method": "content_based"}
            for card_id, score in sorted_cards[:10]
        ]
    
    async def _collaborative_filtering(self, user_id: int, context: Dict) -> List[Dict]:
        """Collaborative filtering based on similar users"""
        if self.interaction_matrix is None:
            return []
        
        # Find similar users
        user_idx = self._get_user_index(user_id)
        if user_idx is None:
            return []
        
        user_similarities = cosine_similarity(
            [self.interaction_matrix[user_idx]], 
            self.interaction_matrix
        )[0]
        
        # Get top similar users
        similar_users = np.argsort(user_similarities)[-6:-1]  # Top 5 similar users
        
        # Get cards liked by similar users
        card_scores = {}
        for similar_user_idx in similar_users:
            similar_user_id = self._get_user_id(similar_user_idx)
            if similar_user_id:
                user_cards = self.user_preferences.get(similar_user_id, {})
                for card_id, score in user_cards.items():
                    if score > 0:  # Only positive interactions
                        card_scores[card_id] = card_scores.get(card_id, 0) + score
        
        sorted_cards = sorted(card_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"card_id": card_id, "score": score, "method": "collaborative"}
            for card_id, score in sorted_cards[:10]
        ]
    
    async def _context_aware_filtering(self, user_id: int, context: Dict) -> List[Dict]:
        """Context-aware filtering based on current situation"""
        merchant = context.get('merchant', '').lower()
        amount = context.get('amount', 0)
        category = context.get('category', '')
        
        card_scores = {}
        
        for card_id, features in self.card_features.items():
            score = 0.0
            
            # Merchant-specific rewards
            if merchant and features.get('merchant_rewards', {}).get(merchant):
                score += features['merchant_rewards'][merchant] * 2
            
            # Category-specific rewards
            if category and features.get('category_rewards', {}).get(category):
                score += features['category_rewards'][category]
            
            # Amount-based optimization
            if amount > 0:
                if amount > 10000 and features.get('high_value_rewards'):
                    score += features['high_value_rewards']
                elif amount < 1000 and features.get('low_value_rewards'):
                    score += features['low_value_rewards']
            
            if score > 0:
                card_scores[card_id] = score
        
        sorted_cards = sorted(card_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"card_id": card_id, "score": score, "method": "context_aware"}
            for card_id, score in sorted_cards[:10]
        ]
    
    async def _rank_recommendations(self, recommendations: List[Dict], 
                                  user_id: int, context: Dict) -> List[Dict]:
        """Rank recommendations using ensemble approach"""
        # Group by card_id and combine scores
        card_scores = {}
        method_counts = {}
        
        for rec in recommendations:
            card_id = rec['card_id']
            if card_id not in card_scores:
                card_scores[card_id] = 0.0
                method_counts[card_id] = 0
            
            # Weight different methods
            method_weights = {
                'content_based': 0.3,
                'collaborative': 0.4,
                'context_aware': 0.3
            }
            
            weight = method_weights.get(rec['method'], 0.1)
            card_scores[card_id] += rec['score'] * weight
            method_counts[card_id] += 1
        
        # Apply diversity penalty for cards with multiple methods
        for card_id in card_scores:
            diversity_bonus = min(method_counts[card_id] * 0.1, 0.3)
            card_scores[card_id] += diversity_bonus
        
        # Sort by final score
        sorted_cards = sorted(card_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                "card_id": card_id,
                "final_score": score,
                "methods_used": method_counts[card_id]
            }
            for card_id, score in sorted_cards
        ]
```

---

*This completes the 100 Gen AI interview questions for a senior architect role, covering all aspects from foundational concepts to advanced implementation patterns based on the SmartCards AI project.*