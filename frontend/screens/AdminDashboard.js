import React from 'react';
import {View, Button} from 'react-native';
import axios from 'axios';
import * as FileSystem from 'expo-file-system';
import * as Sharing from 'expo-sharing';
import * as SecureStore from 'expo-secure-store';

const API = 'http://10.0.2.2:8000';

async function getAuthHeader(){
  const token = await SecureStore.getItemAsync('token');
  return { Authorization: `Bearer ${token}` };
}

export default function AdminDashboard(){
  async function downloadUsers(){
    const h = await getAuthHeader();
    const res = await axios.get(`${API}/users/download/users`, { headers: h, responseType: 'text' });
    const uri = FileSystem.cacheDirectory + 'users.csv';
    await FileSystem.writeAsStringAsync(uri, res.data, { encoding: FileSystem.EncodingType.UTF8 });
    await Sharing.shareAsync(uri);
  }
  async function downloadPosts(){
    const h = await getAuthHeader();
    const res = await axios.get(`${API}/users/download/posts`, { headers: h, responseType: 'text' });
    const uri = FileSystem.cacheDirectory + 'posts.csv';
    await FileSystem.writeAsStringAsync(uri, res.data, { encoding: FileSystem.EncodingType.UTF8 });
    await Sharing.shareAsync(uri);
  }
  return (
    <View style={{padding:20}}>
      <Button title="Download users CSV" onPress={downloadUsers} />
      <View style={{height:12}} />
      <Button title="Download posts CSV" onPress={downloadPosts} />
    </View>
  );
}

export default function AdminDashboard(){
  const [stats,setStats] = useState({});

  useEffect(()=>{
    axios.get(`${API}/admin/stats`).then(r=>setStats(r.data));
  },[]);

  return (
    <View>
      <Text>Users: {stats.users}</Text>
      <Text>Posts: {stats.posts}</Text>
      <Text>Messages: {stats.messages}</Text>
      <Button title="Delete Post" />
      <Button title="Ban User" color="red" />
    </View>
  );
}

