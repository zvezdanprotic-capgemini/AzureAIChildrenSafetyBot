import { useState, useRef, useEffect, useCallback } from 'react';
import {
  VStack,
  Input,
  IconButton,
  Flex,
  useToast,
  Text,
  Badge,
  HStack,
  Button,
} from '@chakra-ui/react';
import { ChatMessage } from './ChatMessage';
import { AgeGate } from './AgeGate';
import { ChatLayout } from './ChatLayout';
import { useAuth } from '../context/AuthContext';
import type { Message } from '../types';
import axios from '../utils/axios';
import { ArrowUpIcon, AddIcon } from '@chakra-ui/icons';

interface HistoryMessage {
  role: string;
  content: string;
  timestamp: number;
  categories?: Record<string, number>;
}

export const ChatContainer = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [age, setAge] = useState<number | null>(null); // fallback if user has no age set
  const [sessionId, setSessionId] = useState<string | null>(null);
  const { token, age: authAge, logout, username } = useAuth();
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const toast = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Create a new session when component mounts
  const createNewSession = useCallback(async () => {
    try {
      const response = await axios.post('/api/chat/session/new', {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSessionId(response.data.session_id);
    } catch (error) {
      console.error('Failed to create new session:', error);
    }
  }, [token]);

  useEffect(() => {
    if (token && !sessionId) {
      createNewSession();
    }
  }, [token, sessionId, createNewSession]);

  const loadChatHistory = async (sessionId: string) => {
    setIsLoadingHistory(true);
    try {
      const response = await axios.get(`/api/chat/history/${sessionId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      const historyMessages: Message[] = response.data.messages.map((msg: HistoryMessage, index: number) => ({
        id: `history-${index}`,
        content: msg.content,
        role: msg.role as 'user' | 'bot',
        timestamp: new Date(msg.timestamp * 1000), // Convert from Unix timestamp
        ageBand: msg.role === 'bot' ? 'adult' : undefined, // Default age band
      }));
      
      setMessages(historyMessages);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    } finally {
      setIsLoadingHistory(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    createNewSession();
  };

  const handleSubmit = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: 'user',
      timestamp: new Date(),
    };

  setMessages((prev) => [...prev, userMessage]);
  // Add provisional typing indicator
  const typingId = `typing-${Date.now()}`;
  setMessages(prev => [...prev, { id: typingId, content: '...', role: 'bot', timestamp: new Date() } as Message]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        message: userMessage.content,
        age: authAge ?? age,
        session_id: sessionId || undefined,
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!sessionId && response.data.session_id) {
        setSessionId(response.data.session_id);
      }

      // Remove typing indicator
      setMessages(prev => prev.filter(m => !m.id.startsWith('typing-')));

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.data.response,
        role: 'bot',
        timestamp: new Date(),
        ageBand: response.data.age_band,
        literacyInjected: response.data.literacy_injected,
        riskLevel: response.data.risk?.risk_level,
        adjusted: /Adjusted to keep things clear and safe/.test(response.data.response)
      };

      if (response.data.moderation_explain) {
        botMessage.moderationExplain = response.data.moderation_explain;
      }

      setMessages((prev) => [...prev, botMessage]);
  } catch {
      toast({
        title: 'Error',
        description: 'Failed to get response from the bot.',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (!token && age === null) {
    return <AgeGate onConfirm={(a) => setAge(a)} />;
  }

  const ageBand = messages.find(m => m.ageBand)?.ageBand || (authAge ? (authAge <=12 ? 'child' : authAge <=17 ? 'teen' : 'adult') : undefined);
  const bandCopy: Record<string, string> = {
    child: 'Hi! I’ll help with fun, safe topics. Ask about science, animals, or words!',
    teen: 'Ask me about learning topics. I’ll keep it safe and suggest help for sensitive issues.',
    adult: 'Safety filters active. I can redirect if a topic isn’t appropriate.'
  };

  const header = (
    <VStack spacing={1} align='flex-start' w='full'>
      <HStack spacing={2} w='full' justify='space-between'>
        <HStack spacing={2}>
          <Text fontWeight='bold'>SafeChat</Text>
          {ageBand && <Badge colorScheme='purple'>{ageBand}</Badge>}
          {sessionId && <Badge fontSize='0.6rem' colorScheme='gray'>sess:{sessionId.slice(0,8)}</Badge>}
        </HStack>
        <HStack spacing={2}>
          <Button
            size='sm'
            leftIcon={<AddIcon />}
            colorScheme='blue'
            variant='outline'
            onClick={startNewChat}
            isLoading={isLoading}
          >
            New Chat
          </Button>
          <Button
            size='sm'
            colorScheme='red'
            variant='outline'
            onClick={() => {
              logout();
              // Optionally redirect to login page
              // navigate('/login');
            }}
            title={`Logout ${username || 'user'}`}
          >
            Logout {username && `(${username})`}
          </Button>
        </HStack>
      </HStack>
      {ageBand && <Text fontSize='xs' color='gray.600'>{bandCopy[ageBand]}</Text>}
    </VStack>
  );

  const messagesList = (
    <VStack align='stretch' spacing={4} aria-live='polite'>
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </VStack>
  );

  const inputBar = (
    <Flex w='full'>
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder='Type your message...'
        onKeyDown={(e) => { if (e.key === 'Enter') handleSubmit(); }}
        mr={2}
      />
      <IconButton
        colorScheme='blue'
        aria-label='Send message'
        icon={<ArrowUpIcon />}
        onClick={handleSubmit}
        isLoading={isLoading}
      />
    </Flex>
  );

  return <ChatLayout header={header} messages={messagesList} inputBar={inputBar} />;
};