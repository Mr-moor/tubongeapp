ws.onmessage = (e) => {
  const data = JSON.parse(e.data);
  if (data.type === "read") {
    setChat(prev =>
      prev.map(m => m.id === data.message_id ? { ...m, delivered: true } : m)
    );
  }
};
