import * as Notifications from 'expo-notifications';

async function registerPush(){
  const token = (await Notifications.getExpoPushTokenAsync()).data;
  return token;
}
