# Individual Project
### Inherited Model: product.template

Created a button called "Update Button".

When clicked, the button triggers a job queue task for the associated product.

The job queue task runs and updates the product that was clicked.

### The task updates the product with the following values:

Name: "Product 1" + Exact timestamp of the click.

Sale Description: "This is the description after the job run" + exact timestamp of the click.

Sales Price: 10.1.

Tax: 19% VAT (If the tax does not exist, it is created first).

### Bonus Features:

Purchase Tax: 15% (If the tax does not exist, it is created first).

Barcode Generation: A function that generates a barcode value and updates the product with this value.