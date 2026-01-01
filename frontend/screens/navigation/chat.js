import { View, TextInput, Button, FlatList, Text } from 'react-native';
import { useEffect, useState } from 'react';
import axios from 'axios';

const API = "http://10.0.2.2:8000";

export default function Chat({ route }) {
  const { userId } = route.params;
  const [msg, setMsg] = useState("");
  const [messages, setMessages] = useState([]);

  async function load() {
    const res = await axios.get(`${API}/messages/${userId}`);
    setMessages(res.data);
  }

  async function send() {
    await axios.post(`${API}/messages`, {
      sender_id: userId,
      receiver_id: 1,
      content: msg
    });
    setMsg("");
    load();
  }

  useEffect(() => { load(); }, []);

  return (
    <View>
      <FlatList
        data={messages}
        keyExtractor={i => i.id.toString()}
        renderItem={({item}) => <Text>{item.content}</Text>}
      />
      <TextInput value={msg} onChangeText={setMsg} />
      <Button title="Send" onPress={send} />
    </View>
  );
}
