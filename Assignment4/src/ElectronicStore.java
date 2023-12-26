import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

public class ElectronicStore {
    private String name;
    private double revenue;
    private double currentTotal;
    private int sales;
    private List<Product> stock;
    private List<Product> currentCart;
    private List<Product> sold;
    private HashMap<Product, Integer> cartQuantities;

    public ElectronicStore(String initName) {
        this.name = initName;
        this.stock = new ArrayList();
        this.revenue = 0.0;
        this.cartQuantities = new HashMap();
        this.currentTotal = 0.0;
        this.currentCart = new ArrayList();
        this.sales = 0;
        this.sold = new ArrayList();
    }

    public double getRevenue() {
        return this.revenue;
    }

    public double getCurrentTotal() {
        return this.currentTotal;
    }

    public int getSales() {
        return this.sales;
    }

    public List<Product> getStock() {
        return this.stock;
    }

    public List<Product> getCurrentCart() {
        return this.currentCart;
    }

    public HashMap<Product, Integer> getCartQuantities() {
        return this.cartQuantities;
    }

    public boolean addProduct(Product newProduct) {
        if (this.stock.contains(newProduct)) {
            return false;
        } else {
            this.stock.add(newProduct);
            return true;
        }
    }

    public static ElectronicStore createStore() {
        ElectronicStore store1 = new ElectronicStore("Watts Up Electronics");
        Desktop d1 = new Desktop(100.0, 10, 3.0, 16, false, 250, "Compact");
        Desktop d2 = new Desktop(200.0, 10, 4.0, 32, true, 500, "Server");
        Laptop l1 = new Laptop(150.0, 10, 2.5, 16, true, 250, 15.0);
        Laptop l2 = new Laptop(250.0, 10, 3.5, 24, true, 500, 16.0);
        Fridge f1 = new Fridge(500.0, 10, 250, "White", "Sub Zero", false);
        Fridge f2 = new Fridge(750.0, 10, 125, "Stainless Steel", "Sub Zero", true);
        ToasterOven t1 = new ToasterOven(25.0, 10, 50, "Black", "Danby", false);
        ToasterOven t2 = new ToasterOven(75.0, 10, 50, "Silver", "Toasty", true);
        store1.addProduct(d1);
        store1.addProduct(d2);
        store1.addProduct(l1);
        store1.addProduct(l2);
        store1.addProduct(f1);
        store1.addProduct(f2);
        store1.addProduct(t1);
        store1.addProduct(t2);
        return store1;
    }

    public List<Product> getMostPopularProducts() {
        List<Product> mostPopularProducts = new ArrayList();
        List<Product> tempList = new ArrayList(this.sold);
        int count = 0;
        Iterator var5;
        Product i;
        if (tempList.isEmpty() || tempList.size() < 3) {
            mostPopularProducts.clear();
            int x = 0;

            for(var5 = tempList.iterator(); var5.hasNext(); ++x) {
                i = (Product)var5.next();
                if (x >= 3) {
                    break;
                }

                mostPopularProducts.add(i);
            }

            for(var5 = this.stock.iterator(); var5.hasNext(); ++x) {
                i = (Product)var5.next();
                if (x >= 3) {
                    break;
                }

                mostPopularProducts.add(i);
            }

            tempList.clear();
        }

        while(!tempList.isEmpty() && count < 3) {
            Product mostSold = (Product)tempList.get(0);
            var5 = tempList.iterator();

            while(var5.hasNext()) {
                i = (Product)var5.next();
                if (i.getSoldQuantity() > mostSold.getSoldQuantity()) {
                    mostSold = i;
                }
            }

            tempList.remove(mostSold);
            mostPopularProducts.add(mostSold);
            ++count;
        }

        return mostPopularProducts;
    }

    public void addToCart(Product product) {
        if (this.cartQuantities.containsKey(product)) {
            int quantity = (Integer)this.cartQuantities.get(product) + 1;
            this.cartQuantities.put(product, quantity);
        } else {
            int quantity = 1;
            this.cartQuantities.put(product, Integer.valueOf(quantity));
            this.currentCart.add(product);
        }

        this.currentTotal += product.getPrice();
        product.setStockQuantity(-1);
        if (product.getStockQuantity() <= 0) {
            this.stock.remove(product);
        }

    }

    public void removeFromCart(Product product) {
        if (this.cartQuantities.containsKey(product)) {
            product.setStockQuantity(1);
            this.currentTotal -= product.getPrice();
            int newQuantity = (Integer)this.cartQuantities.get(product) - 1;
            if (newQuantity > 0) {
                this.cartQuantities.put(product, newQuantity);
            } else {
                this.cartQuantities.remove(product);
                this.currentCart.remove(product);
            }
        }

    }

    public void Buy() {
        if (!this.currentCart.isEmpty()) {
            ++this.sales;
            Iterator var1 = this.cartQuantities.keySet().iterator();

            while(var1.hasNext()) {
                Product i = (Product)var1.next();
                int quantity = (Integer)this.cartQuantities.get(i);
                this.revenue += i.sellUnits(quantity);
                if (!this.sold.contains(i)) {
                    this.sold.add(i);
                }
            }

            this.currentTotal = 0.0;
            this.cartQuantities.clear();
            this.currentCart.clear();
        }

    }
}
