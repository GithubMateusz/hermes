import {BestsellerSection} from "../components/BestsellerSection.jsx";
import {SaleSection} from "../components/SaleSection.jsx";

export default function HomePage() {
    const saleProducts = [

        {
            imageUrl: "products/1.png",
            name: "Product 1",
            key: "product1"
        },
        {
            imageUrl: "products/2.png",
            name: "Product 2",
            key: "product2"
        },
        {
            imageUrl: "products/3.png",
            name: "Product 3",
            key: "product3"
        },
        {
            imageUrl: "products/4.png",
            name: "Product 3",
            key: "product4"
        }
    ]
    const bestsellers = [
        {
            imageUrl: "products/5.png",
            name: "Sukienka Daphne",
            key: "product5"
        },
        {
            imageUrl: "products/6.png",
            name: "Sukienka Molly",
            key: "product6"
        },
        {
            imageUrl: "products/7.png",
            name: "Sukienka Dolly",
            key: "product7"
        },
        {
            imageUrl: "products/8.png",
            name: "Spodnie Mala",
            key: "product8"
        },
    ]
    return (
        <div className="grid gap-10">
            <SaleSection title="WYPRZEDAŻ" products={saleProducts}/>
            <BestsellerSection products={bestsellers}/>
        </div>
    );
}
