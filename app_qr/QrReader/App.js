import { createNativeStackNavigator } from "@react-navigation/native-stack";
const Stack = createNativeStackNavigator();
import { StatusBar } from 'expo-status-bar';
import React, { useEffect } from "react";
import { StyleSheet, Text, View } from 'react-native';
import SplashScreen from "./screens/SplashScreen";
import QrScreen from "./screens/QrScreen";
import { NavigationContainer } from "@react-navigation/native";

export default function App() {



  return (
    <>
      <NavigationContainer>
        <Stack.Navigator screenOptions={{ headerShown: false }}>
            <Stack.Screen
              name="SplashScreen"
              component={SplashScreen}
              options={{ headerShown: false }}
            />
            <Stack.Screen
              name="QrScreen"
              component={QrScreen}
              options={{ headerShown: false }}
            />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
}