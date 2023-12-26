public class Fridge extends Appliance {
    private boolean hasFreezer;

    public Fridge(double initPrice, int initQuantity, int initWattage, String initColor, String initBrand, boolean initFreezer) {
        super(initPrice, initQuantity, initWattage, initColor, initBrand);
        this.hasFreezer = initFreezer;
    }

    public String toString() {
        String result = this.getBrand() + " Fridge ";
        if (this.hasFreezer) {
            result = result + "with Freezer ";
        }

        result = result + "(" + this.getColor() + ", " + this.getWattage() + " watts)";
        return result;
    }
}
