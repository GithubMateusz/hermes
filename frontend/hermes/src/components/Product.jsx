export const Product = ({index, imageUrl, name, show_name, className, imageClassName}) => {

    return (
        <div
            key={index}
            className={`${className}`}
        >
            <img
                src={imageUrl}
                alt={name}
                className={`w-full h-full object-cover object-center ${imageClassName}`}
            />
            {show_name &&
                <div className="p-4 text-center">
                    <h3 className="text-lg font-medium">{name}</h3>
                </div>
            }
        </div>
    )
        ;
}
