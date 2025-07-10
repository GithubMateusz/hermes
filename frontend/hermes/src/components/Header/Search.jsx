export const Search = ({className}) => {
    return (
        <div className={`${className}`}>
            <input
                type="text"
                placeholder="🔍"
                className="full-width bg-[#f4ebe8] placeholder:text-gray-500 text-sm px-3 py-1 rounded-sm border border-transparent focus:outline-none focus:ring-1 focus:ring-[#d2bab2]"
            />
        </div>
    );
}
