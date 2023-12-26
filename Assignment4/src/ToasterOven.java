//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

public class ToasterOven extends Appliance {
    private boolean convection;

    public ToasterOven(double initPrice, int initQuantity, int initWattage, String initColor, String initBrand, boolean initConvection) {
        super(initPrice, initQuantity, initWattage, initColor, initBrand);
        this.convection = initConvection;
    }

    public String toString() {
        String result = this.getBrand() + " Toaster ";
        if (this.convection) {
            result = result + "with convection ";
        }

        result = result + "(" + this.getColor() + ", " + this.getWattage() + " watts)";
        return result;
    }
}