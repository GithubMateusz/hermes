import {Product} from "./Product.jsx";

export const SaleSection = ({title, products}) => {
    return (
        <section className="relative flex justify-center mx-auto">
            <div className="grid grid-cols-2 md:grid-cols-4">
                {products.map((product) => (
                    <Product key={product.key} imageUrl={product.imageUrl} name={product.name} show_name={false}
                             className={"w-70"}/>
                ))}
            </div>

            <h2 className="absolute top-2/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-4xl md:text-8xl font-bold text-[#2C0707]  text-center pointer-events-none">
                {title}
            </h2>
        </section>
    );
};
