import * as Notifications from 'expo-notifications';
import * as SecureStore from 'expo-secure-store';

export async function registerPushToken() {
  const { data: token } = await Notifications.getExpoPushTokenAsync();
  await axios.post(`${API}/users/register_push`, { token });
  await SecureStore.setItemAsync('pushToken', token);
}
