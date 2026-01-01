import * as SecureStore from 'expo-secure-store';
import jwtDecode from 'jwt-decode';

export async function getUserRole(){
  const token = await SecureStore.getItemAsync("token");
  return jwtDecode(token).role;
}

const role = await getUserRole();
if (role === "admin") {
  navigation.replace("AdminDashboard");
} else {
  navigation.replace("Feed");
}
{role === "admin" && (
  <Button title="Admin Panel" onPress={()=>navigation.navigate("AdminDashboard")} />
)}
