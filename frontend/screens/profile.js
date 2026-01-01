export default function Profile(){
  const [email,setEmail] = useState("");

  async function save(){
    await axios.put(`${API}/users/me`, { email });
  }

  return (
    <View>
      <TextInput value={email} onChangeText={setEmail} />
      <Button title="Save" onPress={save} />
    </View>
  );
}
