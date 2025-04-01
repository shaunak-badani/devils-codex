import { useState } from "react";
import { Button } from "@/components/ui/button";
import BackdropWithSpinner from "@/components/ui/backdropwithspinner";
import backendClient from "@/backendClient";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";
import Messages from "./messages";


const Chatbot = () => {

    const [isLoading, setLoading] = useState(false);
    const [query, setQuery] = useState("");
    const [messages, setMessages] = useState([
        { sender: "bot", text: "Hello! How can I assist you today?" },
    ]);

    const handlePromptInput = async(query: string) => {
        if(query === "")
            return;
        const userMessage = {sender: "user", text: query};
        setMessages((prev) => [
            ...prev,
            userMessage
        ]);

        setLoading(true);
        const response = await backendClient.get("/chat", {
            params: {
                query: query
            }
        });
        const chatbotResponse = response.data.answer;
        const chatbotMessage = { sender: "bot", text: chatbotResponse };
        setMessages((prev) => [
            ...prev,
            chatbotMessage
        ]);
        setLoading(false);
        setQuery("");
    } 

    return (
        <>
            <Messages 
                messages={messages}
            />
            <div className="flex items-center gap-2 p-2">
                <Input
                    className="h-12 !text-lg"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="What programs are offered at Duke?"
                />
                <Button onClick={() => handlePromptInput(query)} className="h-12">
                    <Send size={30} />
                </Button>
            </div>
            {isLoading && <BackdropWithSpinner />}
        </>
    )
};


export default Chatbot;