import { useState } from 'react';
import { Box, Button, Input, VStack, Heading, Text } from '@chakra-ui/react';
import axios from '../utils/axios';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const LoginPage = () => {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post('/api/auth/login', { username, password });
      await login(res.data.access_token);
      navigate('/chat');
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <Box maxW="sm" mx="auto" mt={10} p={6} borderWidth={1} borderRadius="lg">
      <VStack spacing={4} align="stretch">
        <Heading size="md">Login</Heading>
        {error && <Text color="red.500" fontSize="sm">{error}</Text>}
        <Input placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <Input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <Button colorScheme="blue" onClick={handleLogin}>Login</Button>
        <Text fontSize="sm">Need an account? <Link to="/register">Register</Link></Text>
      </VStack>
    </Box>
  );
};
