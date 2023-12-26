public abstract class Product {
    private double price;
    private int stockQuantity;
    private int soldQuantity;

    public Product(double initPrice, int initQuantity) {
        this.price = initPrice;
        this.stockQuantity = initQuantity;
        this.soldQuantity = 0;
    }

    public double getPrice() {
        return this.price;
    }

    public int getStockQuantity() {
        return this.stockQuantity;
    }

    public int getSoldQuantity() {
        return this.soldQuantity;
    }

    public void setStockQuantity(int x) {
        this.stockQuantity += x;
    }

    public double sellUnits(int amount) {
        if (amount > 0) {
            this.soldQuantity += amount;
            return this.price * (double)amount;
        } else {
            return 0.0;
        }
    }
}
