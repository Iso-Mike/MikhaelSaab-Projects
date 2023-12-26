public abstract class Appliance extends Product {
    private int wattage;
    private String color;
    private String brand;

    public Appliance(double initPrice, int initQuantity, int initWattage, String initColor, String initBrand) {
        super(initPrice, initQuantity);
        this.wattage = initWattage;
        this.color = initColor;
        this.brand = initBrand;
    }

    public String getColor() {
        return this.color;
    }

    public String getBrand() {
        return this.brand;
    }

    public int getWattage() {
        return this.wattage;
    }
}
