   function ChatbotWidget() {
      const [messages, setMessages] = React.useState([
        { text: "Hello! How can I assist you today?", sender: "bot" }
      ]);
      const [input, setInput] = React.useState("");
  
      const sendMessage = () => {
        if (!input.trim()) return;
        const newMessages = [...messages, { text: input, sender: "user" }];
        setMessages(newMessages);
        setInput("");
  
        setTimeout(() => {
          setMessages(prev => [...prev, { text: "I'm just a demo bot!", sender: "bot" }]);
        }, 1000);
      };
  
      return (
        <div style={{
          width: "300px", position: "fixed", bottom: "20px", right: "20px", 
          backgroundColor: "white", borderRadius: "10px", boxShadow: "0px 0px 10px rgba(0,0,0,0.1)", 
          padding: "10px", display: "flex", flexDirection: "column"
        }}>
          <h3 style={{ textAlign: "center", margin: "0 0 10px 0" }}>Chatbot</h3>
          <div style={{ flex: 1, overflowY: "auto", maxHeight: "300px", padding: "5px", borderBottom: "1px solid #ddd" }}>
            {messages.map((msg, index) => (
              <div key={index} style={{
                padding: "5px", borderRadius: "5px", margin: "5px 0",
                backgroundColor: msg.sender === "bot" ? "#f1f1f1" : "#007bff", 
                color: msg.sender === "bot" ? "#000" : "#fff", 
                alignSelf: msg.sender === "bot" ? "flex-start" : "flex-end"
              }}>
                {msg.text}
              </div>
            ))}
          </div>
          <div style={{ display: "flex", marginTop: "10px" }}>
            <input 
              type="text" value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Type a message..." 
              style={{ flex: 1, padding: "5px", borderRadius: "5px", border: "1px solid #ccc" }}
            />
            <button onClick={sendMessage} style={{
              marginLeft: "5px", padding: "5px 10px", backgroundColor: "#007bff", 
              color: "white", borderRadius: "5px", border: "none"
            }}>Send</button>
          </div>
        </div>
      );
    }

ReactDOM.render(<ChatbotWidget />, document.getElementById("chatbot-widget"));
export default ChatbotWidget;