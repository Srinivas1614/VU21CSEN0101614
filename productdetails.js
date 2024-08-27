import React from 'react';

function ProductDetails({ product }) {
  if (!product) return <div>No Product Selected</div>;

  return (
    <div>
      <h1>{product.productName}</h1>
      <p>Price: ${product.price}</p>
      <p>Rating: {product.rating}</p>
      <p>Discount: {product.discount}%</p>
      <p>Availability: {product.availability}</p>
    </div>
  );
}

export default ProductDetails;
