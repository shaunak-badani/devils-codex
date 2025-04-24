import { 
    Select, 
    SelectContent, 
    SelectGroup, 
    SelectItem, 
    SelectLabel, 
    SelectTrigger, 
    SelectValue 
} from "@/components/ui/select";


const SelectPrompt = (props: any) => {

    const prompts = [
        "Get me a list of courses offered for the AIPI program",
        "Who is the instructor for Modeling Processes and Algorithms",
        "What documents are required to apply to the MEng AI program?"
    ]

    const { setPrompt } = props;

    return (
        <div className="flex justify-center my-5">
            <Select onValueChange={setPrompt}>
                <SelectTrigger className="w-1/2">
                <SelectValue placeholder="See example prompts!" />
                </SelectTrigger>
                <SelectContent>
                <SelectGroup>
                    <SelectLabel>Example prompts</SelectLabel>
                    {prompts.map((prompt, idx) => 
                        <SelectItem key={idx} value={prompt}>{prompt}</SelectItem>
                    )}
                </SelectGroup>
                </SelectContent>
            </Select>
        </div>
    );
};

export default SelectPrompt