import React, { useState, useEffect, useRef } from "react";
import { Container, Row, Col, Card, Form, Button, InputGroup, Spinner, Modal } from "react-bootstrap";

function App() {
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [showSettings, setShowSettings] = useState(false);
  const messagesEndRef = useRef(null);

  // Load API Key from local storage if available
  useEffect(() => {
    const savedKey = localStorage.getItem("GROQ_API_KEY");
    if (savedKey) setApiKey(savedKey);
    else setShowSettings(true); // Ask for key if not found
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSaveKey = () => {
    localStorage.setItem("GROQ_API_KEY", apiKey);
    setShowSettings(false);
  };

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!inputValue.trim()) return;

    if (!apiKey) {
      setShowSettings(true);
      return;
    }

    const userMessage = inputValue;
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInputValue("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({ message: userMessage, history: history }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
        setHistory(data.history);
      } else {
        setMessages((prev) => [...prev, { role: "error", content: data.error || "An error occurred" }]);
        if (response.status === 401) {
             setShowSettings(true);
        }
      }
    } catch (error) {
      setMessages((prev) => [...prev, { role: "error", content: "Network error. Make sure the backend server is running." }]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setHistory([]);
  };

  return (
    <div style={{ backgroundColor: "#f4f6f9", minHeight: "100vh", display: "flex", alignItems: "center" }}>
      <Container className="py-4">
        <Row className="justify-content-center">
          <Col md={10} lg={8}>
            <Card className="shadow-lg border-0 rounded-4" style={{ height: "85vh", display: "flex", flexDirection: "column" }}>
              <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center py-3 rounded-top-4 border-0">
                <h5 className="mb-0 fw-bold"><i className="bi bi-robot me-2"></i> PyBot AI</h5>
                <div>
                  <Button variant="light" size="sm" className="me-2 rounded-circle" onClick={clearChat} title="Clear Chat">
                    <i className="bi bi-trash-fill text-danger"></i>
                  </Button>
                  <Button variant="light" size="sm" className="rounded-circle" onClick={() => setShowSettings(true)} title="Settings">
                    <i className="bi bi-gear-fill text-primary"></i>
                  </Button>
                </div>
              </Card.Header>
              
              <Card.Body className="overflow-auto p-4" style={{ backgroundColor: "#fff" }}>
                {messages.length === 0 && (
                  <div className="text-center text-muted mt-5">
                    <i className="bi bi-chat-dots" style={{ fontSize: "3rem", color: "#dee2e6" }}></i>
                    <p className="mt-3 fs-5">Start chatting with PyBot!</p>
                  </div>
                )}
                {messages.map((msg, idx) => (
                  <div key={idx} className={`d-flex mb-3 ${msg.role === "user" ? "justify-content-end" : "justify-content-start"}`}>
                    <div 
                      className={`p-3 rounded-4 shadow-sm`}
                      style={{ 
                        maxWidth: "75%", 
                        backgroundColor: msg.role === "user" ? "#0d6efd" : msg.role === "error" ? "#f8d7da" : "#f1f3f5",
                        color: msg.role === "user" ? "#fff" : msg.role === "error" ? "#842029" : "#212529",
                        borderBottomRightRadius: msg.role === "user" ? "0" : "1rem",
                        borderBottomLeftRadius: msg.role !== "user" ? "0" : "1rem",
                        whiteSpace: "pre-wrap"
                      }}
                    >
                      {msg.role === "assistant" && <strong><i className="bi bi-robot me-2"></i></strong>}
                      {msg.content}
                    </div>
                  </div>
                ))}
                {loading && (
                  <div className="d-flex mb-3 justify-content-start">
                    <div className="p-3 rounded-4 bg-light shadow-sm" style={{ borderBottomLeftRadius: "0" }}>
                      <Spinner animation="grow" size="sm" className="me-1 text-secondary" />
                      <Spinner animation="grow" size="sm" className="me-1 text-secondary" style={{ animationDelay: "0.2s" }} />
                      <Spinner animation="grow" size="sm" className="text-secondary" style={{ animationDelay: "0.4s" }} />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </Card.Body>
              
              <Card.Footer className="bg-white border-top-0 p-3 rounded-bottom-4">
                <Form onSubmit={handleSend}>
                  <InputGroup className="shadow-sm rounded-pill p-1 border">
                    <Form.Control
                      type="text"
                      placeholder="Type your message..."
                      className="border-0 bg-transparent rounded-pill px-4"
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      disabled={loading}
                      style={{ boxShadow: "none" }}
                    />
                    <Button type="submit" variant="primary" className="rounded-pill px-4" disabled={loading || !inputValue.trim()}>
                      <i className="bi bi-send-fill"></i>
                    </Button>
                  </InputGroup>
                </Form>
              </Card.Footer>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Settings Modal */}
      <Modal show={showSettings} onHide={() => setShowSettings(false)} centered>
        <Modal.Header closeButton className="border-0">
          <Modal.Title className="fw-bold"><i className="bi bi-key-fill text-warning me-2"></i> API Key Settings</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="text-muted mb-4">To use PyBot, you need to provide your Groq API Key. Your key is stored securely in your browser and never sent to our servers.</p>
          <Form.Group className="mb-3">
            <Form.Label className="fw-bold">Groq API Key</Form.Label>
            <Form.Control 
              type="password" 
              placeholder="gsk_..." 
              value={apiKey} 
              onChange={(e) => setApiKey(e.target.value)} 
              className="p-3"
            />
            <Form.Text className="text-muted">
              Don&apos;t have one? Get it for free at <a href="https://console.groq.com/keys" target="_blank" rel="noreferrer">console.groq.com</a>.
            </Form.Text>
          </Form.Group>
        </Modal.Body>
        <Modal.Footer className="border-0 pt-0">
          <Button variant="primary" onClick={handleSaveKey} className="w-100 rounded-pill py-2 fw-bold">
            Save Key & Continue
          </Button>
        </Modal.Footer>
      </Modal>

    </div>
  );
}

export default App;
