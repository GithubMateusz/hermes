import {Product} from "./Product.jsx";

export const BestsellerSection = ({products}) => {
    return (
        <section className="grid gap-10">
            <h2 className="text-4xl font-bold text-center">Bestsellery</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-24 justify-items-center ">
                {products.map((product, index) => (
                    <Product key={product.key} imageUrl={product.imageUrl} name={product.name} index={index} show_name={true}
                             className={"w-50"} imageClassName={"rounded-md"}/>
                ))}
            </div>
        </section>
    );
};
