import React, {useState} from 'react';
import {View, TextInput, Button, Text, StyleSheet} from 'react-native';
import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API = 'http://10.0.2.2:8000';

export default function LoginScreen({navigation}){
  const [id, setId] = useState('');
  const [pw, setPw] = useState('');
  const [err, setErr] = useState(null);

  async function onLogin(){
    try{
      const form = new URLSearchParams();
      form.append('username', id);
      form.append('password', pw);
      const res = await axios.post(`${API}/auth/token`, form);
      const token = res.data.access_token;
      await SecureStore.setItemAsync('token', token);
      navigation.replace('Feed');
    }catch(e){
      setErr('Login failed');
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tubonge</Text>
      <TextInput style={styles.input} placeholder="username or email" value={id} onChangeText={setId} />
      <TextInput style={styles.input} placeholder="password" secureTextEntry value={pw} onChangeText={setPw} />
      {err && <Text style={{color:'red'}}>{err}</Text>}
      <Button title="Log in" onPress={onLogin} />
    </View>
  );
}

const styles = StyleSheet.create({
  container:{flex:1, padding:20, justifyContent:'center'},
  input:{borderWidth:1, borderColor:'#ddd', padding:12, borderRadius:8, marginBottom:12},
  title:{fontSize:28, fontWeight:'700', marginBottom:20, textAlign:'center'}
});

import React, { useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { API } from '../api/api';
import Input from '../components/Input';

export default function LoginScreen({ navigation }) {
  const [id, setId] = useState('');
  const [pw, setPw] = useState('');
  const [err, setErr] = useState(null);

  async function login() {
    try {
      const form = new URLSearchParams();
      form.append('username', id);
      form.append('password', pw);

      const res = await API.post('/auth/token', form);
      await SecureStore.setItemAsync('token', res.data.access_token);

      navigation.replace('Feed');

    } catch (e) {
      setErr("Invalid login");
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tubonge</Text>

      <Input placeholder="Username or email" value={id} onChange={setId} />
      <Input placeholder="Password" secure value={pw} onChange={setPw} />

      {err && <Text style={{ color: 'red' }}>{err}</Text>}

      <TouchableOpacity style={styles.btn} onPress={login}>
        <Text style={styles.btnText}>Login</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate("Register")}>
        <Text style={styles.link}>Create account</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate("AdminRegister")}>
        <Text style={styles.link}>Admin registration</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container:{ flex:1, justifyContent:'center', padding:20 },
  title:{ fontSize:32, fontWeight:'800', marginBottom:30, textAlign:'center' },
  btn:{ backgroundColor:'#2e86de', padding:15, borderRadius:10, marginTop:10 },
  btnText:{ color:'#fff', fontSize:18, textAlign:'center' },
  link:{ color:'#2e86de', textAlign:'center', marginTop:15 }
});
