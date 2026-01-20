import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, SafeAreaView, ScrollView, TextInput, Alert } from 'react-native';
import { PaperProvider, Card, Button } from 'react-native-paper';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import API_BASE_URL from './src/config/api';

interface Project {
  id: number;
  project_name: string;
  project_type: string;
  location: string;
}

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    checkLogin();
  }, []);

  const checkLogin = async () => {
    try {
      const savedToken = await AsyncStorage.getItem('token');
      if (savedToken) {
        setToken(savedToken);
        setLoggedIn(true);
        loadProjects(savedToken);
      }
    } catch (error) {
      console.error('Error checking login:', error);
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please enter username and password');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post($RAILWAY_URL/api/v1/auth/login, formData);
      const accessToken = response.data.access_token;
      
      await AsyncStorage.setItem('token', accessToken);
      setToken(accessToken);
      setLoggedIn(true);
      loadProjects(accessToken);
    } catch (error: any) {
      Alert.alert('Login Failed', error.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const loadProjects = async (authToken: string) => {
    try {
      const response = await axios.get($RAILWAY_URL/api/v1/projects/, {
        headers: { Authorization: Bearer  }
      });
      setProjects(response.data);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const handleLogout = async () => {
    await AsyncStorage.removeItem('token');
    setLoggedIn(false);
    setToken(null);
    setProjects([]);
    setUsername('');
    setPassword('');
  };

  if (!loggedIn) {
    return (
      <PaperProvider>
        <SafeAreaView style={styles.container}>
          <ScrollView contentContainerStyle={styles.loginContainer}>
            <Text style={styles.title}>CEDOS</Text>
            <Text style={styles.subtitle}>Civil Engineering Digital Operating System</Text>
            
            <Card style={styles.card}>
              <Card.Content>
                <TextInput
                  style={styles.input}
                  placeholder="Username"
                  value={username}
                  onChangeText={setUsername}
                  autoCapitalize="none"
                />
                <TextInput
                  style={styles.input}
                  placeholder="Password"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                />
                <Button
                  mode="contained"
                  onPress={handleLogin}
                  loading={loading}
                  style={styles.loginButton}
                >
                  Login
                </Button>
              </Card.Content>
            </Card>
            
            <Text style={styles.info}>API: https://cedos-architect-production.up.railway.app</Text>
          </ScrollView>
        </SafeAreaView>
      </PaperProvider>
    );
  }

  return (
    <PaperProvider>
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>CEDOS</Text>
          <Button mode="text" onPress={handleLogout}>Logout</Button>
        </View>
        
        <ScrollView style={styles.content}>
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.sectionTitle}>My Projects ({projects.length})</Text>
              {projects.length === 0 ? (
                <Text style={styles.emptyText}>No projects yet. Create one from the web app!</Text>
              ) : (
                projects.map((project) => (
                  <View key={project.id} style={styles.projectItem}>
                    <Text style={styles.projectName}>{project.project_name}</Text>
                    <Text style={styles.projectType}>{project.project_type}</Text>
                    <Text style={styles.projectLocation}>{project.location}</Text>
                  </View>
                ))
              )}
            </Card.Content>
          </Card>
          
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.sectionTitle}>Quick Actions</Text>
              <Button mode="contained" style={styles.actionButton} onPress={() => Alert.alert('Info', 'Use web app for full features')}>
                View Dashboard
              </Button>
              <Button mode="outlined" style={styles.actionButton} onPress={() => Alert.alert('Info', 'Use web app for full features')}>
                Create Project
              </Button>
              <Button mode="outlined" style={styles.actionButton} onPress={() => Alert.alert('Info', 'Use web app for full features')}>
                Calculator
              </Button>
            </Card.Content>
          </Card>
        </ScrollView>
      </SafeAreaView>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loginContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#1976d2',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  card: {
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  loginButton: {
    marginTop: 10,
  },
  info: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
    marginTop: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#1976d2',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  projectItem: {
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginBottom: 10,
  },
  projectName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  projectType: {
    fontSize: 14,
    color: '#666',
    marginBottom: 3,
  },
  projectLocation: {
    fontSize: 12,
    color: '#999',
  },
  emptyText: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
    textAlign: 'center',
    padding: 20,
  },
  actionButton: {
    marginBottom: 10,
  },
});
