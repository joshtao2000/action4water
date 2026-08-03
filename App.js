import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';

import AuthScreen from './screens/AuthScreen';
import MapScreen from './screens/MapScreen';
import SettingsScreen from './screens/SettingsScreen';
import LoadingScreen from './screens/LoadingScreen';
import ResultsScreen from './screens/ResultsScreen';
import SavedScreen from './screens/SavedScreen';
import AboutScreen from './screens/AboutScreen';
import FieldReportScreen from './screens/FieldReportScreen';

const Stack = createStackNavigator();
const API_URL = 'https://northern-lakes-api.onrender.com';

export default function App() {
  const [initialRoute, setInitialRoute] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const email = await AsyncStorage.getItem('user_email');
        if (email) {
          // Fire login count update in background
          fetch(`${API_URL}/app-login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email }),
          }).catch(() => {});
          setInitialRoute('Map');
        } else {
          setInitialRoute('Auth');
        }
      } catch (e) {
        setInitialRoute('Auth');
      }
    })();
  }, []);

  if (!initialRoute) {
    return (
      <View style={styles.splash}>
        <Text style={styles.title}>Northern Lakes{'\n'}Watch</Text>
        <Text style={styles.sub}>Satellite-based lake monitoring</Text>
        <ActivityIndicator color="#fff" size="large" style={{ marginTop: 40 }} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName={initialRoute}
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name="Auth" component={AuthScreen} />
        <Stack.Screen name="Map" component={MapScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
        <Stack.Screen name="Loading" component={LoadingScreen} />
        <Stack.Screen name="Results" component={ResultsScreen} />
        <Stack.Screen name="Saved" component={SavedScreen} />
        <Stack.Screen name="About" component={AboutScreen} />
        <Stack.Screen name="Report" component={FieldReportScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  splash: {
    flex: 1, backgroundColor: '#0F6E56',
    alignItems: 'center', justifyContent: 'center', padding: 32,
  },
  title: {
    fontSize: 36, fontWeight: '700', color: '#fff',
    textAlign: 'center', lineHeight: 44, marginBottom: 12,
  },
  sub: { fontSize: 16, color: 'rgba(255,255,255,0.75)', textAlign: 'center' },
});
