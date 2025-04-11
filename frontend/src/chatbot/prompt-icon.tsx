import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { cn } from "@/lib/utils";


const PromptIcon = (props: any) => {

    const { image, leftMargin } = props;
    
    return (
        <div className={cn(leftMargin ? "ml-2 sm:ml-2" : "mr-2 sm:mr-2", "my-auto")}>
            <Avatar className="">
                <AvatarImage src={image} />
                <AvatarFallback>CN</AvatarFallback>
            </Avatar>
        </div>
    )
}

export default PromptIcon;