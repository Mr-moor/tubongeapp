import React, {useEffect, useState} from 'react';
import {View, Text, FlatList, Image} from 'react-native';
import { MotiView } from 'moti';
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API = 'http://10.0.2.2:8000';

async function getAuthHeader(){
  const token = await SecureStore.getItemAsync('token');
  return { Authorization: `Bearer ${token}` };
}

export default function FeedScreen(){
  const [posts, setPosts] = useState([]);
  useEffect(()=>{ fetchFeed(); },[])

  async function fetchFeed(){
    const h = await getAuthHeader();
    const res = await axios.get(`${API}/posts/feed`, { headers: h });
    setPosts(res.data);
  }

  const renderItem = ({item}) => (
    <MotiView from={{opacity:0, translateY:20}} animate={{opacity:1, translateY:0}} transition={{type:'timing', duration:350}} style={{margin:12, background:'#fff', borderRadius:12, padding:10}}>
      <Text style={{fontWeight:'600'}}>{item.content_text}</Text>
      {item.media_url && <Image source={{uri:item.media_url}} style={{height:200, borderRadius:10, marginTop:8}} />}
    </MotiView>
  )

  return <FlatList data={posts} keyExtractor={p=>String(p.id)} renderItem={renderItem} />;
}

export default function Feed(){
  const [posts, setPosts] = useState([]);

  async function load(){
    const res = await axios.get(`${API}/posts`);
    setPosts(res.data);
  }

  useEffect(()=>{ load(); },[]);

  return (
    <FlatList
      data={posts}
      renderItem={({item})=>(
        <View>
          <Text>{item.content}</Text>
          <Button title={`❤️ ${item.likes}`} />
        </View>
      )}
    />
  );
}
