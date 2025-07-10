import {FaShoppingCart, FaUser} from "react-icons/fa";
import {Menu} from "./Menu.jsx";
import {LinkWithIcon} from "./LinkWithIcon.jsx";
import {Search} from "./Search.jsx";
import {Logo} from "./Logo.jsx";

export const Header = ({items}) => {

    return (
        <header className="bg-white shadow-lg font-bold">
            <div className="flex w-full items-center justify-between pl-10 pr-10 py-2">
                <div className="flex gap-12 items-end justify-between pt-8 pb-6">
                    <Logo/>
                    <Menu items={items}/>
                </div>

                {/* Right */}
                <div className="grid grid-cols-2 gap-4 ">
                    <LinkWithIcon
                        icon={<FaUser />}
                        text="Profil"
                    />
                    <LinkWithIcon
                        icon={<FaShoppingCart/>}
                        text="Koszyk"
                    />

                    <Search className="col-span-2"/>
                </div>
            </div>
        </header>);
};
