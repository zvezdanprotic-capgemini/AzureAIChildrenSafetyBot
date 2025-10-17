import { Box, Flex, IconButton, Fade, Tooltip } from '@chakra-ui/react';
import { ReactNode, useRef, useEffect, useState, useCallback } from 'react';
import { ArrowDownIcon } from '@chakra-ui/icons';

interface ChatLayoutProps {
  header: ReactNode;
  messages: ReactNode;
  inputBar: ReactNode;
}

export const ChatLayout = ({ header, messages, inputBar }: ChatLayoutProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [atBottom, setAtBottom] = useState(true);
  const [pendingNew, setPendingNew] = useState(false);

  const isNearBottom = () => {
    const el = scrollRef.current;
    if (!el) return true;
    return el.scrollHeight - el.scrollTop - el.clientHeight < 120;
  };

  const handleScroll = useCallback(() => {
    if (isNearBottom()) {
      setAtBottom(true);
      setPendingNew(false);
    } else {
      setAtBottom(false);
    }
  }, []);

  const scrollToBottom = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
    setAtBottom(true);
    setPendingNew(false);
  }, []);

  // Auto-scroll only if user near bottom
  useEffect(() => {
    if (isNearBottom()) {
      scrollToBottom();
    } else {
      setPendingNew(true);
    }
  }, [messages, scrollToBottom]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    el.addEventListener('scroll', handleScroll);
    return () => el.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  return (
    <Flex direction='column' w='100%' maxW='860px' mx='auto' h='75vh' borderWidth={1} borderRadius='lg' overflow='hidden' boxShadow='md' bg='white'>
      <Box px={4} py={3} borderBottom='1px solid' borderColor='gray.200' bg='gray.50'>
        {header}
      </Box>
      <Box ref={scrollRef} flex={1} overflowY='auto' p={4} bg='gray.25' position='relative'>
        {messages}
        <Fade in={pendingNew && !atBottom} unmountOnExit>
          <Tooltip label='New messages'>
            <IconButton
              aria-label='Scroll to newest messages'
              icon={<ArrowDownIcon />}
              size='sm'
              colorScheme='blue'
              position='absolute'
              bottom={4}
              right={4}
              onClick={scrollToBottom}
              boxShadow='md'
            />
          </Tooltip>
        </Fade>
      </Box>
      <Box px={4} py={3} borderTop='1px solid' borderColor='gray.200' bg='gray.50'>
        {inputBar}
      </Box>
    </Flex>
  );
};
