import { useState } from 'react';
import { Box, Button, Select, Text, VStack } from '@chakra-ui/react';

type Props = { onConfirm: (age: number) => void };

export const AgeGate = ({ onConfirm }: Props) => {
  const [age, setAge] = useState<number>(13);
  return (
    <Box borderWidth={1} borderRadius="lg" p={6} maxW="md" mx="auto" mt={10}>
      <VStack spacing={4} align="stretch">
        <Text fontSize="lg" fontWeight="bold">Welcome!</Text>
        <Text fontSize="sm">Please select your age so we can keep this chat safe and appropriate.</Text>
        <Select value={age} onChange={(e) => setAge(parseInt(e.target.value, 10))}>
          {Array.from({ length: 100 }, (_, i) => i + 1).map(a => (
            <option key={a} value={a}>{a}</option>
          ))}
        </Select>
        <Button colorScheme="blue" onClick={() => onConfirm(age)}>Continue</Button>
        <Text fontSize="xs" color="gray.500">We do not store personal data. Age is only used to adjust safety filters.</Text>
      </VStack>
    </Box>
  );
};
