import { Alert, AlertIcon, AlertTitle, Tooltip, HStack, Text } from '@chakra-ui/react';

interface SafeNoticeProps {
  reason: string;
  categories?: Record<string, number>;
}

const reasonMap: Record<string, string> = {
  content_safety_block: 'Blocked for safety',
  jailbreak_detected: 'Attempt blocked',
};

export const SafeNotice = ({ reason, categories }: SafeNoticeProps) => {
  const label = reasonMap[reason] || 'Safety Notice';
  return (
    <Alert status='warning' variant='subtle' p={2} borderRadius='md'>
      <AlertIcon />
      <HStack spacing={2} align='flex-start'>
        <AlertTitle fontSize='sm'>{label}</AlertTitle>
        {categories && (
          <Tooltip label={Object.entries(categories).map(([k,v]) => `${k}: ${v}`).join('\n')} fontSize='xs'>
            <Text fontSize='xs' color='gray.600'>details</Text>
          </Tooltip>
        )}
      </HStack>
    </Alert>
  );
};
