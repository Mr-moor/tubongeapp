import React from 'react';
import { TextInput, StyleSheet } from 'react-native';

export default function Input({ placeholder, secure, value, onChange }) {
  return (
    <TextInput 
      style={styles.input}
      placeholder={placeholder}
      secureTextEntry={secure}
      value={value}
      onChangeText={onChange}
    />
  );
}

const styles = StyleSheet.create({
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 12,
    borderRadius: 10,
    marginBottom: 12,
    fontSize: 16
  }
});
