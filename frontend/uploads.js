import * as ImagePicker from 'expo-image-picker';

const pick = async () => {
  const img = await ImagePicker.launchImageLibraryAsync();
  const data = new FormData();
  data.append("file", {
    uri: img.assets[0].uri,
    name: "upload.jpg",
    type: "image/jpeg"
  });
  await axios.post(`${API}/upload`, data);
};

import * as ImagePicker from 'expo-image-picker';
import axios from 'axios';

export async function pickAndUpload(roomId) {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.All,
    quality: 0.5, // compress
  });

  const form = new FormData();
  form.append("file", {
    uri: result.assets[0].uri,
    type: result.assets[0].type,
    name: result.assets[0].uri.split("/").pop(),
  });

  await axios.post(`${API}/upload/${roomId}`, form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}
