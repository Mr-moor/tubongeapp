import AsyncStorage from '@react-native-async-storage/async-storage';

await AsyncStorage.setItem("feed", JSON.stringify(posts));
const cached = await AsyncStorage.getItem("feed");
