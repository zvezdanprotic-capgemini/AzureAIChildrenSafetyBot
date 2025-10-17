import { useState } from 'react';
import { 
  Box, 
  Button, 
  Input, 
  VStack, 
  Heading, 
  Text, 
  NumberInput, 
  NumberInputField,
  Alert,
  AlertIcon,
  FormControl,
  FormLabel,
  FormHelperText,
  FormErrorMessage
} from '@chakra-ui/react';
import axios from '../utils/axios';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ValidationError {
  type: string;
  loc: string[];
  msg: string;
  input: unknown;
  ctx?: Record<string, unknown>;
}

export const RegisterPage = () => {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [age, setAge] = useState<number | undefined>();
  const [error, setError] = useState<string | null>(null);
  const [validationErrors, setValidationErrors] = useState<ValidationError[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async () => {
    setError(null);
    setValidationErrors([]);
    setIsLoading(true);

    try {
      const res = await axios.post('/api/auth/register', { username, password, age });
      await login(res.data.access_token);
      navigate('/chat');
    } catch (e: unknown) {
      const error = e as { response?: { status?: number; data?: { detail?: string | ValidationError[] } } };
      if (error.response?.status === 422) {
        // Validation errors
        setValidationErrors((error.response.data?.detail as ValidationError[]) || []);
        setError('Please fix the validation errors below');
      } else {
        setError(error.response?.data?.detail as string || 'Registration failed');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const getFieldError = (fieldName: string) => {
    return validationErrors.find(err => err.loc?.includes(fieldName))?.msg;
  };

  const isUsernameValid = username.length >= 3;
  const isPasswordValid = password.length >= 6;

  return (
    <Box maxW="sm" mx="auto" mt={10} p={6} borderWidth={1} borderRadius="lg">
      <VStack spacing={4} align="stretch">
        <Heading size="md">Register</Heading>
        
        {error && (
          <Alert status="error" size="sm">
            <AlertIcon />
            {error}
          </Alert>
        )}

        <FormControl isInvalid={!!getFieldError('username')}>
          <FormLabel>Username</FormLabel>
          <Input 
            placeholder="Username" 
            value={username} 
            onChange={e => setUsername(e.target.value)}
          />
          <FormHelperText>Must be at least 3 characters</FormHelperText>
          <FormErrorMessage>{getFieldError('username')}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!getFieldError('password')}>
          <FormLabel>Password</FormLabel>
          <Input 
            placeholder="Password" 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)}
          />
          <FormHelperText>Must be at least 6 characters</FormHelperText>
          <FormErrorMessage>{getFieldError('password')}</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!getFieldError('age')}>
          <FormLabel>Age (optional)</FormLabel>
          <NumberInput min={1} max={120} onChange={(_, v) => setAge(v || undefined)}>
            <NumberInputField placeholder="Age (optional)" />
          </NumberInput>
          <FormHelperText>Helps us provide age-appropriate responses</FormHelperText>
          <FormErrorMessage>{getFieldError('age')}</FormErrorMessage>
        </FormControl>

        <Button 
          colorScheme="blue" 
          onClick={handleRegister}
          isLoading={isLoading}
          isDisabled={!isUsernameValid || !isPasswordValid}
        >
          Create Account
        </Button>
        
        <Text fontSize="sm">Already have an account? <Link to="/login">Login</Link></Text>
      </VStack>
    </Box>
  );
};
