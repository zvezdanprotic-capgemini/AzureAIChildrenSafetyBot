import { Box, Text, Badge, VStack, HStack, Tooltip, IconButton } from '@chakra-ui/react';
import { CopyIcon } from '@chakra-ui/icons';
import type { Message } from '../types';
import { SafeNotice } from './SafeNotice';

type ChatMessageProps = {
  message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.role === 'user';
  return (
    <VStack
      maxW="80%"
      mb={4}
      alignSelf={isUser ? 'flex-end' : 'flex-start'}
      spacing={1}
      align={isUser ? 'flex-end' : 'flex-start'}
    >
      <HStack spacing={2}>
        {!isUser && message.ageBand && (
          <Badge colorScheme='purple' variant='subtle'>{message.ageBand}</Badge>
        )}
        {message.adjusted && (
            <Tooltip label='Adjusted for safety (phrasing normalized)'>
              <Badge colorScheme='orange'>adjusted</Badge>
            </Tooltip>
        )}
        {message.literacyInjected && (
          <Badge colorScheme='teal'>tip</Badge>
        )}
        {message.riskLevel && message.riskLevel !== 'low' && (
          <Badge colorScheme={message.riskLevel === 'high' ? 'red' : 'yellow'}>{message.riskLevel} risk</Badge>
        )}
      </HStack>
      <Box
        bg={isUser ? 'blue.500' : 'gray.100'}
        color={isUser ? 'white' : 'gray.800'}
        p={4}
        borderRadius='lg'
        boxShadow='sm'
        w='full'
        position='relative'
        aria-label={isUser ? 'User message' : 'Assistant message'}
      >
        <Text whiteSpace='pre-wrap'>{message.content}</Text>
        {!isUser && message.content !== '...' && (
          <IconButton
            aria-label='Copy message'
            icon={<CopyIcon />}
            size='xs'
            variant='ghost'
            position='absolute'
            top={1}
            right={1}
            onClick={() => navigator.clipboard.writeText(message.content)}
          />
        )}
        <Text fontSize='xs' color={isUser ? 'whiteAlpha.700' : 'gray.500'} mt={2}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </Text>
      </Box>
      {message.moderationExplain && (
        <SafeNotice reason={message.moderationExplain.reason} categories={message.moderationExplain.categories} />
      )}
    </VStack>
  );
};