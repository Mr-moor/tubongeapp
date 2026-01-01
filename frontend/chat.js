import { useEffect, useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';

export default function Chat(){
  const [msg, setMsg] = useState("");
  const [chat, setChat] = useState([]);
  const ws = new WebSocket("ws://10.0.2.2:8000/ws/chat");

  useEffect(()=>{
    ws.onmessage = e => setChat(prev => [...prev, e.data]);
    return () => ws.close();
  }, []);

  return (
    <View>
      {chat.map((c,i)=><Text key={i}>{c}</Text>)}
      <TextInput value={msg} onChangeText={setMsg}/>
      <Button title="Send" onPress={()=>{ ws.send(msg); setMsg(""); }} />
    </View>
  );
}

import { encrypt, decrypt } from '../utils/crypto';

ws.send(encrypt(msg));

ws.onmessage = e => {
  setChat(prev => [...prev, decrypt(e.data)]);
};
