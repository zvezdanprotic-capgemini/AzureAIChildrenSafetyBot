import { ChakraProvider, Container, Button, Flex, Spacer, Text } from '@chakra-ui/react';
import React from 'react';
import { ChatContainer } from './components/ChatContainer';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { LogoutPage } from './pages/LogoutPage';
import { AuthProvider, useAuth } from './context/AuthContext';

const Protected: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const { token } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  return children;
};

function App() {
  return (
    <ChakraProvider>
      <AuthProvider>
        <BrowserRouter>
          <TopNav />
          <Container maxW="container.lg" py={6}>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/logout" element={<LogoutPage />} />
              <Route path="/chat" element={<Protected><ChatContainer /></Protected>} />
              <Route path="*" element={<Navigate to="/chat" replace />} />
            </Routes>
          </Container>
        </BrowserRouter>
      </AuthProvider>
    </ChakraProvider>
  )
}

const TopNav = () => {
  const { token, username } = useAuth();
  return (
    <Flex px={6} py={3} bg="gray.50" borderBottom="1px solid" borderColor="gray.200" align="center" gap={4}>
      <Text fontWeight="bold"><Link to="/chat">SafeChat Demo</Link></Text>
      <Spacer />
      {!token && (
        <Flex gap={3}>
          <Button size="sm" as={Link} to="/login">Login</Button>
          <Button size="sm" as={Link} to="/register" colorScheme="blue">Register</Button>
        </Flex>
      )}
      {token && (
        <Flex gap={3} align="center">
          <Text fontSize="sm">{username}</Text>
          <Button size="sm" variant="outline" as={Link} to="/logout">Logout</Button>
        </Flex>
      )}
    </Flex>
  );
};

export default App
