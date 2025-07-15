

const MenuItem = ({name}) => {
    return (
        <li className={`hover:text-[#5e4740] cursor-pointer`}>
            {name}
        </li>
    );
}


export const Menu = ({items, className}) => {

    return (

        <nav>
            <ul className={`flex gap-12 ${className}`}>
                {items.map((item, index) => (
                    <MenuItem
                        key={index}
                        name={item.name}
                    />
                ))}
            </ul>
        </nav>
    );
};
