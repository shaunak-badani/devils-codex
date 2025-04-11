import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"


const PromptIcon = (props: any) => {

    const { image } = props;
    
    return (
        <div className="mr-2 sm:mr-2 my-auto">
            <Avatar className="">
                <AvatarImage src={image} />
                <AvatarFallback>CN</AvatarFallback>
            </Avatar>
        </div>
    )
}

export default PromptIcon;