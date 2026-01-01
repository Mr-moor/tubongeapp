import CryptoJS from "crypto-js";

const SECRET = "tubonge-chat-key";

export function encrypt(text){
  return CryptoJS.AES.encrypt(text, SECRET).toString();
}

export function decrypt(cipher){
  const bytes = CryptoJS.AES.decrypt(cipher, SECRET);
  return bytes.toString(CryptoJS.enc.Utf8);
}
