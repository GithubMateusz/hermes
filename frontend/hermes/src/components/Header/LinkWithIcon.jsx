export const LinkWithIcon = ({icon, text, className}) => {
    return (
        <div
            className={`flex items-center gap-2 cursor-pointer hover:text-[#5e4740] ${className}`}
        >
            {icon}
            <span className=" font-medium">{text}</span>
        </div>
    );
}
