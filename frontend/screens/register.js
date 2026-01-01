import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { API } from '../api/api';
import Input from '../components/Input';

export default function RegisterScreen({ navigation }) {
  const [u, setU] = useState('');
  const [e, setE] = useState('');
  const [p, setP] = useState('');
  const [msg, setMsg] = useState(null);

  async function register() {
    try {
      await API.post('/users/register', {
        username: u,
        email: e,
        password: p
      });
      setMsg("Account created!");
    } catch {
      setMsg("Registration failed.");
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create Account</Text>

      <Input placeholder="Username" value={u} onChange={setU} />
      <Input placeholder="Email" value={e} onChange={setE} />
      <Input placeholder="Password" secure value={p} onChange={setP} />

      <TouchableOpacity style={styles.btn} onPress={register}>
        <Text style={styles.btnText}>Register</Text>
      </TouchableOpacity>

      {msg && <Text style={{textAlign:'center', marginTop:10}}>{msg}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container:{ flex:1, justifyContent:'center', padding:20 },
  title:{ fontSize:28, fontWeight:'700', marginBottom:25, textAlign:'center' },
  btn:{ backgroundColor:'#27ae60', padding:15, borderRadius:10, marginTop:10 },
  btnText:{ color:'#fff', fontSize:18, textAlign:'center' },
});
