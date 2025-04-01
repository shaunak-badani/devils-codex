

const Messages = (props: any) => {

    const { messages } = props;

    return (
        <div className="py-2 sm:py-2 my-2 sm:my-2">
            {messages.map((msg: any) => {
                const isUser = msg['sender'] === "user";
                const justifyEnd = isUser ? "justify-end" : "";
                const bgColor = isUser? "#00539B" : "#988675";
                return (
                <>
                    <div className={`flex ${justifyEnd}`}>
                        <div key={msg['text']} className={`text-xl bg-[${bgColor}] text-white
                     w-3/5 py-2 sm:py-2 rounded-sm my-3 sm:my-3`}>
                            <h1>{msg['text']}</h1>
                        </div>
                    </div>
                </>
                )})
            }
        </div>
    )
};

export default Messages;