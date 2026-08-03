import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import LaunchScreen from './screens/LaunchScreen';
import AuthScreen from './screens/AuthScreen';
import MapScreen from './screens/MapScreen';
import SettingsScreen from './screens/SettingsScreen';
import LoadingScreen from './screens/LoadingScreen';
import ResultsScreen from './screens/ResultsScreen';
import SavedScreen from './screens/SavedScreen';
import AboutScreen from './screens/AboutScreen';
import FieldReportScreen from './screens/FieldReportScreen';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Launch"
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name="Launch" component={LaunchScreen} />
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
