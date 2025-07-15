import {LinkWithIcon} from "./LinkWithIcon.jsx";
import {FaShoppingCart, FaUser} from "react-icons/fa";
import {Search} from "./Search.jsx";
import {Logo} from "./Logo.jsx";


const MenuItem = ({name}) => {
    return (
        <li className={`hover:text-[#5e4740] cursor-pointer center`}>
            {name}
        </li>
    );
}


export const Menu = ({items, className}) => {
    return (
        <nav className={`flex flex-grow ${className}`}>
            <ul className="flex flex-col justify-center flex-grow gap-4 items-center md:flex-row md:items-end md:justify-between">
                <li>
                    <Logo/>
                </li>
                {items.map((item, index) => (
                    <MenuItem
                        key={index}
                        name={item.name}
                    />
                ))}
                <li className="flex-col gap-4">
                    <div className="flex justify-between gap-4 pl-2 pr-2">
                        <LinkWithIcon
                            icon={<FaUser/>}
                            text="Profil"
                        />
                        <LinkWithIcon
                            icon={<FaShoppingCart/>}
                            text="Koszyk"
                        />
                    </div>

                    <Search className="col-span-2"/>
                </li>
            </ul>
        </nav>
    );
};
