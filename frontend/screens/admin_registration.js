import React, { useState } from 'react';
import { ScrollView, StyleSheet, Alert } from 'react-native';
import { TextInput, Button, Title, Text } from 'react-native-paper';
import axios from 'axios';

const API = 'http://10.0.2.2:8000'; // FastAPI backend

export default function AdminRegister({ navigation }) {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [secretCode, setSecretCode] = useState('');
  const [err, setErr] = useState(null);

  const onRegister = async () => {
    try {
      const res = await axios.post(`${API}/admin/register`, {
        full_name: fullName,
        email,
        username,
        phone,
        password,
        secret_code: secretCode,
      });
      Alert.alert("Success", res.data.message, [
        { text: "OK", onPress: () => navigation.replace('AdminDashboard') }
      ]);
    } catch (error) {
      console.log(error.response?.data);
      setErr(error.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Title style={styles.title}>Register Admin</Title>

      <TextInput label="Full Name" mode="outlined" value={fullName} onChangeText={setFullName} style={styles.input} />
      <TextInput label="Email" mode="outlined" keyboardType="email-address" value={email} onChangeText={setEmail} style={styles.input} />
      <TextInput label="Username" mode="outlined" value={username} onChangeText={setUsername} style={styles.input} />
      <TextInput label="Phone" mode="outlined" keyboardType="phone-pad" value={phone} onChangeText={setPhone} style={styles.input} />
      <TextInput label="Password" mode="outlined" secureTextEntry value={password} onChangeText={setPassword} style={styles.input} />
      <TextInput label="Secret Code" mode="outlined" secureTextEntry value={secretCode} onChangeText={setSecretCode} style={styles.input} />

      {err && <Text style={styles.error}>{err}</Text>}

      <Button mode="contained" onPress={onRegister} style={styles.button}>Register Admin</Button>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, padding: 20, justifyContent: 'center', backgroundColor: '#f7f9fc' },
  title: { textAlign: 'center', marginBottom: 20, fontSize: 28 },
  input: { marginBottom: 12, backgroundColor: 'white' },
  button: { marginTop: 10, padding: 8 },
  error: { color: 'red', marginBottom: 10, textAlign: 'center' },
});
