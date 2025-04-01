import './App.css'
import { Card } from "@/components/ui/card"
import Chatbot from './chatbot/chatbot'

function App() {

  return (
    <>
      <div>
        <div className="header p-6 text-xl border-b">Devil's Codex</div>
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
