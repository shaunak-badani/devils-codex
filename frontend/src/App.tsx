import './App.css'
import { Card } from "@/components/ui/card"
import Chatbot from './chatbot/chatbot'
import logo from "./assets/Duke_Official_Codex.png"

function App() {

  return (
    <>
      <div>
          <div className="py-12 sm:py-12 font-extrabold lg:text-5xl border-b">Devil's Codex</div>
          <div className="min-h-screen p-8 pb-8 sm:p-8">      
            <main className="max-w-4xl mx-auto flex flex-col gap-16">
              <div>
                <Card className="p-20">
                  <Chatbot />
                </Card>
              </div>
            </main>
          </div>
      </div>
    </>
  )
}

export default App
