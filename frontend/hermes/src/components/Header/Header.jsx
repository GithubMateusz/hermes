import {Menu} from "./Menu.jsx";

export const Header = ({items}) => {

    return (
        <header className="bg-white shadow-lg font-bold pl-10 pr-10 py-2 pt-8 pb-6">
            <div className="flex w-full items-center justify-between gap-10">
                <Menu items={items}/>
            </div>
        </header>);
};
