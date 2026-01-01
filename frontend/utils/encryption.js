import CryptoJS from "crypto-js";

export const encrypt = (text, key) =>
  CryptoJS.AES.encrypt(text, key).toString();

export const decrypt = (cipher, key) =>
  CryptoJS.AES.decrypt(cipher, key).toString(CryptoJS.enc.Utf8);
