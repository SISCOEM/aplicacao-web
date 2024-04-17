import React, { useState, useEffect } from "react";
import { Text, View, StyleSheet, Button, Dimensions, Image, TouchableOpacity } from "react-native";
import { CameraView, Camera } from "expo-camera/next";
import { Color, FontFamily, FontSize } from "../GlobalStyles";
import * as SecureStore from 'expo-secure-store';
import { Audio } from 'expo-av';

const { height: screenHeight, width: screenWidth } = Dimensions.get('window');

export default function App() {
  console.log(typeof Audio);
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [definingUrl, setDefiningUrl] = useState(false);
  const [url, setUrl] = useState('');
  
  let soundObject;

  const loadSound = async () => {
    if (!soundObject) {
      soundObject = new Audio.Sound();
      await soundObject.loadAsync(require('../assets/passSound.mp3'));
    }
  };

  const playSound = async () => {
    await loadSound();

    try {
      await soundObject.playAsync();
    } catch (error) {
      console.error('Erro ao reproduzir o som', error);
    }
  };
  
  useEffect(() => {
    const getCameraPermissions = async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    };

    const setUrlSystem = async () => {
      let data = await SecureStore.getItemAsync('url');
      console.log(data);

      if (data) {
        setUrl(data);
      } else {
        setDefiningUrl(true);
      }
    }

    getCameraPermissions();
    setUrlSystem();
  }, []);

  const handleBarCodeScanned = async ({ type, data }) => {
    setScanned(true);
    playSound();

    if (definingUrl){
      if (data.startsWith("http://")) {
        await SecureStore.setItemAsync("url", data);
        setUrl(data);
        setDefiningUrl(false);
        alert("Url definido com sucesso!");
      } else {
        alert("Qr code inválido: " + data);
      }
    } else {
      if (url) {
        if (!(data.startsWith("http://"))) {
          fetch(`${url}equipamento/set?uid=${data}`)
            .catch(() => {alert("Conexão com o sistema perdida!")});
        } else {
          alert("Qr code inválido: " + data);
        }
      } else {
        alert("Defina uma url primeiramente!");
      }
    }

    setTimeout(() => {
      setScanned(false);
    }, 2000);
  };

  if (hasPermission === null) {
    return <Text>Requesting for camera permission</Text>;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  let styleBorderColor = {
    borderColor: scanned ? 'gray' : 'white',
  }

  return (
    <View style={styles.container}>
      <CameraView
        onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
        barcodeScannerSettings={{
          barCodeTypes: ["qr", "pdf417"],
        }}
        style={StyleSheet.absoluteFillObject}
      />
      <View style={styles.nav}>
        <Image source={require('../assets/logo.png')} style={styles.logo} />
        <Text style={styles.text}>SISCOEM</Text>
      </View>
      <View style={styles.navBottom}>
        <TouchableOpacity
          style={[styles.button, {backgroundColor: definingUrl ? "gray" : "white"}]}
          onPress={() => {if (!definingUrl) setDefiningUrl(true);}}
        >
          <Image source={require('../assets/linkIcon.png')} style={styles.urlIcon}/>
          <Text style={styles.textButton}>Redefinir url</Text>
        </TouchableOpacity>
      </View>
      <View style={styles.squares}>
        <View style={styles.top}>
          <View style={[styles.squareTopLeft, styles.squareBorder, styleBorderColor]}/>
          <View style={[styles.squareTopRight, styles.squareBorder, styleBorderColor]}/>
        </View>
        <View style={styles.bottom}>
          <View style={[styles.squareBottomLeft, styles.squareBorder, styleBorderColor]}/>
          <View style={[styles.squareBottomRight, styles.squareBorder, styleBorderColor]}/>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    justifyContent: "center",
  },
  squareBorder: {
    height: screenWidth * 0.15,
    width: screenWidth * 0.15,
    borderColor: "white",
  },
  squares: {
    height: screenWidth * 0.5,
    width: screenWidth * 0.5,
    position: "absolute",
    flexDirection: "column",
    justifyContent: 'space-between',
  },
  squareTopLeft: {
    borderTopWidth: 2,
    borderLeftWidth: 2,
    borderTopLeftRadius: 20.
  },
  squareTopRight: {
    borderTopWidth: 2,
    borderRightWidth: 2,
    borderTopRightRadius: 20,
  },
  squareBottomRight: {
    borderBottomWidth: 2,
    borderRightWidth: 2,
    borderBottomRightRadius: 20,
  },
  squareBottomLeft: {
    borderLeftWidth: 2,
    borderBottomWidth: 2,
    borderBottomLeftRadius: 20,
  },
  top: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: "100%",
  },
  bottom: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: "100%",
  },
  nav: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Color.colorBg,
    height: screenHeight * 0.1,
    width: screenWidth,
    position: 'absolute',
    top: 0,
    zIndex: 100,
  },
  button: {
    height: screenHeight * 0.05,
    backgroundColor: "white",
    paddingLeft: 20,
    paddingRight: 20,
    paddingTop: 10,
    paddingBottom: 10,
    borderRadius: 10,
    flexDirection: 'row',
  },
  navBottom: {
    flexDirection: 'row',
    alignItems: 'center',
    display: 'flex',
    justifyContent: 'center',
    backgroundColor: Color.colorBg,
    height: screenHeight * 0.1,
    width: screenWidth,
    position: 'absolute',
    bottom: 0,
    zIndex: 100,
  },
  textButton: {
    fontSize: 20,
    fontWeight: "bold",
    color: Color.colorBg,
    marginRight: 10,
  },
  text: {
    color: "white",
    fontSize: screenHeight * 0.04,
    fontWeight: "bold",
  },
  logo: {
    marginRight: 30,
    height: screenHeight * 0.09,
    width: screenHeight * 0.09,
    backgroundColor: "#8d7a68",
    borderRadius: 40
  },
  urlIcon: {
    height: 40, 
    width: 40,
    marginRight: 10,
  }
});