import React, { useEffect } from 'react';
import { View, Image, StyleSheet } from 'react-native';
import { Color } from "../GlobalStyles";

const SplashScreen = ({ navigation }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      navigation.reset({
        index: 0,
        routes: [{ name: "QrScreen" }],
      });
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigation]);

  return (
    <View style={styles.container}>
      <Image source={require('../assets/logo.png')} style={styles.logo} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: Color.colorBg,
  },
  logo: {
    width: 550,
    height: 550,
    resizeMode: 'contain',
  },
});

export default SplashScreen;
